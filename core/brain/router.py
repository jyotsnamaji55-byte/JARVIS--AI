import os
import requests

from core.brain.backup import ask_backup

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"


def ask_groq(messages, timeout=30):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "GROQ_API_KEY is not configured."
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages
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
        content = data["choices"][0]["message"]["content"]

        return {
            "success": True,
            "content": content,
            "provider": "Groq",
            "model": GROQ_MODEL
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": f"Groq network/API error: {error}"
        }

    except (KeyError, IndexError, TypeError, ValueError) as error:
        return {
            "success": False,
            "error": f"Groq response error: {error}"
        }


def ask_brain(messages, timeout=30):
    primary = ask_groq(messages, timeout=timeout)

    if primary["success"]:
        return primary

    backup = ask_backup(messages, timeout=timeout)

    if backup["success"]:
        backup["fallback_from"] = "Groq"
        backup["primary_error"] = primary.get("error")
        return backup

    return {
        "success": False,
        "error": "Both primary and backup AI providers failed.",
        "primary_error": primary.get("error"),
        "backup_error": backup.get("error")
    }
