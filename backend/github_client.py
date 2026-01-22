import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_issue(repo_url: str, issue_number: int) -> dict:
    # Extract owner and repo
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]

    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    # -------------------------
    # Fetch issue
    # -------------------------
    issue_response = requests.get(issue_url, headers=headers)

    if issue_response.status_code != 200:
        raise Exception(
            f"GitHub API error ({issue_response.status_code}): {issue_response.text}"
        )

    try:
        issue_data = issue_response.json()
    except ValueError:
        raise Exception("GitHub returned a non-JSON response for issue details")

    # -------------------------
    # Fetch comments
    # -------------------------
    comments_url = issue_data.get("comments_url")
    comments = []

    if comments_url:
        comments_response = requests.get(comments_url, headers=headers)

        if comments_response.status_code != 200:
            raise Exception("Failed to fetch comments from GitHub")

        try:
            comments_data = comments_response.json()
            comments = [c.get("body", "") for c in comments_data]
        except ValueError:
            raise Exception("GitHub returned a non-JSON response for comments")

    return {
        "title": issue_data.get("title", ""),
        "body": issue_data.get("body") or "",
        "comments": comments
    }
