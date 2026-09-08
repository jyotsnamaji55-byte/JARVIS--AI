import os
import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"


def generate_upgrade(request, file_path, current_code, timeout=60):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "GROQ_API_KEY is not configured."
        }

    prompt = f"""
You are JARVIS Upgrade Planner.

Upgrade request:
{request}

Target Python file:
{file_path}

Current code:
{current_code}

Design a safe upgrade for the requested feature.

Rules:
- Return only the complete proposed Python source code.
- Preserve existing functionality.
- Do not use shell commands.
- Do not access files outside the JARVIS project.
- Do not modify environment variables or API keys.
- Do not add destructive or security-bypass behavior.
- Keep the code syntactically valid.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Generate safe, maintainable Python code for the JARVIS project."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=timeout
        )

        response.raise_for_status()

        data = response.json()
        code = data["choices"][0]["message"]["content"].strip()

        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]

        if code.endswith("```"):
            code = code[:-3]

        return {
            "success": True,
            "file": file_path,
            "code": code.strip(),
            "model": MODEL
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": f"Upgrade generation network/API error: {error}"
        }

    except (KeyError, IndexError, TypeError, ValueError) as error:
        return {
            "success": False,
            "error": f"Upgrade generation response error: {error}"
        }
