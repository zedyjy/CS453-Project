import requests
from app.config import GITHUB_TOKEN, GITHUB_API_URL

def fetch_pr_diff(owner: str, repo: str, pr_number: int) -> str:
    """
    Fetches a PR diff from GitHub using a Personal Access Token.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
        "User-Agent": "LLM-CodeReview-Bot"
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"GitHub API error [{response.status_code}]: {response.text}")
        return ""

