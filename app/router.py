from app.services.reviewer import review_with_openai, review_with_deepseek
from fastapi import APIRouter, Request
from app.services.github_integration import fetch_pr_diff, post_review_comment

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    if "pull_request" in payload and payload["action"] in ["opened", "reopened", "synchronize"]:
        pr_info = payload["pull_request"]
        pr_url = pr_info["html_url"]  # e.g. https://github.com/user/repo/pull/123
        comments_url = pr_info["comments_url"]  # URL to post comments to

        # Extract owner, repo, and number from URL
        parts = pr_url.split("/")
        owner = parts[3]
        repo = parts[4]
        pr_number = int(parts[6])

        print(f"Fetching PR #{pr_number} from {owner}/{repo}")
        diff = fetch_pr_diff(owner, repo, pr_number)

        print("PR Diff Preview:\n", diff[:500])

        # Get AI review
        open_review = review_with_openai(diff)

        deep_review = review_with_deepseek(diff)



        # Post review as comment
        post_review_comment(comments_url, open_review, "OpenAI")

        post_review_comment(comments_url, deep_review, "DeepSeek")

        return {
            "message": "PR diff fetched",
            "pr_number": pr_number,
            "repo": f"{owner}/{repo}",
        }

    return {"message": "Not a pull request event"}
