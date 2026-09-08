import os
import requests

from core.personality import JARVIS_PERSONALITY
from core.memory.manager import save_memory, get_memories, delete_memory
from core.memory.context import build_memory_context
from core.memory.intelligence import remember_from_text
from tools.registry.defaults import create_default_registry
from core.agent.controller import AgenticController
from core.agent.loop import AgenticLoop
from core.automation.runner import AutomationRunner

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

tool_registry = create_default_registry()
agent = AgenticController(tool_registry)
agent_loop = AgenticLoop(agent)
automation = AutomationRunner()

messages = [
    {
        "role": "system",
        "content": JARVIS_PERSONALITY
    }
]


def handle_memory_command(message):
    text = message.strip()

    if text.lower().startswith("remember "):
        data = text[9:].strip()

        if "=" not in data:
            return "JARVIS: Use format: remember key = value"

        key, value = data.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key or not value:
            return "JARVIS: Both key and value are required."

        save_memory(key, value)
        return f"JARVIS: Memory saved — {key} = {value}"

    if text.lower().startswith("recall "):
        key = text[7:].strip()

        if not key:
            return "JARVIS: Please provide a memory key."

        memories = get_memories(key)

        if not memories:
            return f"JARVIS: I don't have a memory for '{key}'."

        return f"JARVIS: {key} = {memories[0]}"

    if text.lower().startswith("forget "):
        key = text[7:].strip()

        if not key:
            return "JARVIS: Please provide a memory key."

        delete_memory(key)
        return f"JARVIS: Memory deleted — {key}"

    return None


def handle_tool_command(message):
    text = message.strip()

    if text.lower().startswith("code "):
        request = text[5:].strip()

        if not request:
            return "JARVIS: Please describe what code you want me to generate."

        tool = tool_registry.get("generate_code")
        result = tool["function"](request)

        if not result["success"]:
            return f"JARVIS: Coding Engine error — {result['error']}"

        return "JARVIS: Code generated and validated successfully.\n\n" + result["code"]

    return None


def ask_jarvis(message):
    if not os.getenv("GROQ_API_KEY"):
        print("JARVIS: API key is not configured.")
        return

    remember_from_text(message)

    memory_reply = handle_memory_command(message)

    if memory_reply:
        return memory_reply

    tool_reply = handle_tool_command(message)

    if tool_reply:
        return tool_reply

    if message.lower().startswith("agent "):
        goal = message[6:].strip()

        if not goal:
            return "JARVIS: Please describe the goal."

        result = agent_loop.run(goal)

        if not result["success"]:
            return (
                "JARVIS: Agentic loop failed.\n"
                + str(result.get("error", "Unknown error."))
            )

        last = result["history"][-1]["result"]

        summary = (
            "JARVIS: Agentic loop completed successfully.\n\n"
            f"Goal: {goal}\n"
            f"Iterations: {result['iterations']}\n"
            f"Tools: {last['agent']['tools']}\n"
            f"Plan steps: {len(last['agent']['plan'])}\n"
        )

        for execution in last['agent'].get('results', []):
            tool_result = execution.get('result')

            if (
                execution.get('tool') == 'calculator'
                and isinstance(tool_result, dict)
                and tool_result.get('success') is True
            ):
                summary += f"Result: {tool_result.get('result')}\n"

        return summary

    memory_context = build_memory_context(message)

    user_content = message

    if memory_context:
        user_content = (
            f"{memory_context}\n\n"
            f"Current user message:\n{message}\n\n"
            "Use the relevant memories when helpful. "
            "Do not invent memories."
        )

    messages.append({
        "role": "user",
        "content": user_content
    })

    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    if "choices" not in result or not result["choices"]:
        print("JARVIS: I received an unexpected AI response.")
        return

    reply = result["choices"][0]["message"]["content"]

    messages.append({
        "role": "assistant",
        "content": reply
    })

    return reply


def main():
    print("JARVIS AI is online.")
    print("Context memory: ON")
    print("Persistent memory: ON")
    print("Type 'exit' to shut down.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("JARVIS: Shutting down.")
            break

        try:
            reply = ask_jarvis(user_input)

            if reply:
                print(reply)

        except requests.exceptions.Timeout:
            print("JARVIS: The AI service took too long to respond. Please try again.")

        except requests.exceptions.RequestException:
            print("JARVIS: I could not connect to the AI service.")

        except Exception:
            print("JARVIS: Something unexpected happened.")


if __name__ == "__main__":
    main()

