import os
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openrouter/free"


def ask_backup(messages, timeout=30):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "OPENROUTER_API_KEY is not configured."
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
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
            "provider": "OpenRouter",
            "model": OPENROUTER_MODEL
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": f"Backup network/API error: {error}"
        }

    except (KeyError, IndexError, TypeError, ValueError) as error:
        return {
            "success": False,
            "error": f"Backup response error: {error}"
        }
