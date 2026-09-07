import os
import requests


API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"


def generate_python_code(request):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "success": False,
            "code": None,
            "error": "GROQ_API_KEY is not configured."
        }

    prompt = f"""
You are JARVIS Coding Engine.

Generate clean, readable Python code for this request:

{request}

Rules:
- Return only Python source code.
- Do not use Markdown code fences.
- Do not execute anything.
- Do not include explanations outside the code.
- Keep the code focused on the user's request.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You generate safe, focused Python source code."
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
            API_URL,
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        code = result["choices"][0]["message"]["content"].strip()

        return {
            "success": True,
            "code": code,
            "error": None
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "code": None,
            "error": "AI request timed out."
        }

    except requests.exceptions.RequestException as error:
        return {
            "success": False,
            "code": None,
            "error": f"AI request failed: {error}"
        }

    except (KeyError, IndexError, TypeError):
        return {
            "success": False,
            "code": None,
            "error": "Unexpected AI response."
        }
