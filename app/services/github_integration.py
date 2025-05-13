import requests
from app.config import GITHUB_TOKEN, GITHUB_API_URL

def fetch_pr_diff(owner: str, repo: str, pr_number: int) -> str:
    """
    Fetches the unified diff of a pull request using GitHub's diff media type.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
        "User-Agent": "DualReview-Bot"
    }

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ GitHub API error while fetching diff: {e}")
        return ""


def post_review_comment(comments_url: str, review_text: str, commenter: str) -> bool:
    """
    Posts a markdown-formatted review comment to a GitHub pull request.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DualReview-Bot"
    }

    payload = {
        "body": f"### 🧠 {commenter} Code Review\n\n{review_text}"
    }

    try:
        response = requests.post(comments_url, json=payload, headers=headers)
        if response.status_code == 201:
            print(f"✅ Successfully posted review from {commenter}")
            return True
        else:
            print(f"⚠️ Failed to post comment [{response.status_code}]: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"❌ GitHub comment post error: {e}")
        return False
