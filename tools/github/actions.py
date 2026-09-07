import os
import requests

GITHUB_API = "https://api.github.com"


def trigger_workflow(repo, workflow, ref="main"):
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        return {
            "success": False,
            "error": "GITHUB_TOKEN is not configured."
        }

    url = f"{GITHUB_API}/repos/{repo}/actions/workflows/{workflow}/dispatches"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    payload = {"ref": ref}

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 204:
            return {
                "success": True,
                "message": "GitHub workflow triggered successfully.",
                "repo": repo,
                "workflow": workflow,
                "ref": ref,
            }

        return {
            "success": False,
            "error": f"GitHub API returned HTTP {response.status_code}: {response.text}"
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": f"GitHub API/network error: {error}"
        }
