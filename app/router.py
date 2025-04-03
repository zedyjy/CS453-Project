from app.services.reviewer import review_with_openai
from fastapi import APIRouter, Request
from app.services.github_integration import fetch_pr_diff

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    if "pull_request" in payload:
        pr_info = payload["pull_request"]
        pr_url = pr_info["html_url"]  # e.g. https://github.com/user/repo/pull/123

        # Extract owner, repo, and number from URL
        parts = pr_url.split("/")
        owner = parts[3]
        repo = parts[4]
        pr_number = int(parts[6])

        print(f"Fetching PR #{pr_number} from {owner}/{repo}")
        diff = fetch_pr_diff(owner, repo, pr_number)

        print("PR Diff Preview:\n", diff[:500])
        
        return {
            "message": "PR diff fetched",
            "pr_number": pr_number,
            "repo": f"{owner}/{repo}",
        }

    return {"message": "Not a pull request event"}
