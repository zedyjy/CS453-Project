from fastapi import APIRouter, Request
from app.services.config_handler import CONFIG_CACHE, handle_config_comment
from app.services.github_integration import fetch_pr_diff, post_review_comment
from app.services.reviewer import review_with_openai, review_with_deepseek

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    # 1️⃣ Handle configuration comments to trigger a review with user preferences
    if "comment" in payload and payload.get("action") == "created":
        comment_body = payload["comment"]["body"]
        if comment_body.strip().startswith("@DualReview configure"):
            await handle_config_comment(payload)

            # Extract context for PR
            repo_info = payload["repository"]
            owner = repo_info["owner"]["login"]
            repo = repo_info["name"]
            pr_number = payload["issue"]["number"]
            comments_url = payload["issue"]["comments_url"]
            pr_url = payload["issue"]["pull_request"]["url"]

            # Fetch diff and run review with custom settings
            diff = fetch_pr_diff(owner, repo, pr_number)
            config = CONFIG_CACHE.get(pr_url, {})
            model = config.get("preferred_model", "gpt-4o")
            focus = config.get("focus", ["security", "readability"])
            strictness = config.get("strictness", "medium")

            if model == "gpt-4o":
                review = review_with_openai(diff, focus, strictness)
                post_review_comment(comments_url, review, "OpenAI")
            elif model == "deepseek":
                review = review_with_deepseek(diff, focus, strictness)
                post_review_comment(comments_url, review, "DeepSeek")
            else:
                open_review = review_with_openai(diff, focus, strictness)
                deep_review = review_with_deepseek(diff, focus, strictness)
                post_review_comment(comments_url, open_review, "OpenAI")
                post_review_comment(comments_url, deep_review, "DeepSeek")

            return {"message": "Configuration applied and review posted"}

    # 2️⃣ Handle PR opened: only onboarding, wait for configure comment
    if "pull_request" in payload and payload.get("action") == "opened":
        pr_info = payload["pull_request"]
        pr_url = pr_info["url"]
        comments_url = pr_info["comments_url"]

        if not CONFIG_CACHE.get(pr_url, {}).get("onboarded"):
            onboarding_msg = """👋 **Hi! I'm DualReview — your automated AI code reviewer.**

I analyze pull requests using **GPT-4o** and **DeepSeek**.

You can customize your review preferences by commenting:

```bash
@DualReview configure
{
  "preferred_model": "gpt-4o",
  "focus": ["security", "performance"],
  "strictness": "high"
}
```

---

🤖 `preferred_model` options:
- "gpt-4o" — use OpenAI’s GPT-4o
- "deepseek" — use DeepSeek’s model  
*(if omitted, both are used)*

🎯 `focus` options:
- "security", "readability", "performance", "bug-risk", "maintainability", "test-coverage", "documentation", "best-practices"

⚙️ `strictness`:
- "low" – only major issues
- "medium" – balanced review
- "high" – includes nits and style tips

---

You can update these anytime by re-commenting.  

_I will wait for your comment before reviewing._

Happy reviewing with **DualReview**! 🚀
"""
            post_review_comment(comments_url, onboarding_msg, "DualReview")
            CONFIG_CACHE.setdefault(pr_url, {})["onboarded"] = True

        return {"message": "Onboarding sent"}

    # 3️⃣ Handle PR reopened or synchronized: run default review + onboarding if first time
    if "pull_request" in payload and payload.get("action") in ["synchronize"]:
        pr_info = payload["pull_request"]
        pr_url = pr_info["url"]
        pr_number = pr_info["number"]
        comments_url = pr_info["comments_url"]
        html_url = pr_info["html_url"]

        # Extract owner and repo
        parts = html_url.split("/")
        owner = parts[3]
        repo = parts[4]

        # Run default review
        diff = fetch_pr_diff(owner, repo, pr_number)
        config = CONFIG_CACHE.get(pr_url, {})
        model = config.get("preferred_model", "gpt-4o")
        focus = config.get("focus", ["security", "readability"])
        strictness = config.get("strictness", "medium")

        if model == "gpt-4o":
            review = review_with_openai(diff, focus, strictness)
            post_review_comment(comments_url, review, "OpenAI")
        elif model == "deepseek":
            review = review_with_deepseek(diff, focus, strictness)
            post_review_comment(comments_url, review, "DeepSeek")
        else:
            open_review = review_with_openai(diff, focus, strictness)
            deep_review = review_with_deepseek(diff, focus, strictness)
            post_review_comment(comments_url, open_review, "OpenAI")
            post_review_comment(comments_url, deep_review, "DeepSeek")

        # Onboarding if not yet sent
        if not CONFIG_CACHE.get(pr_url, {}).get("onboarded"):
            onboarding_msg = """👋 **Hi! I'm DualReview — your automated AI code reviewer.**

I analyze pull requests using **GPT-4o** and **DeepSeek**.

To customize your review, please comment:

```bash
@DualReview configure
{
  "preferred_model": "gpt-4o",
  "focus": ["security", "performance"],
  "strictness": "high"
}
```

_I will wait for your comment before reviewing._
"""
            post_review_comment(comments_url, onboarding_msg, "DualReview")
            CONFIG_CACHE.setdefault(pr_url, {})["onboarded"] = True

        return {"message": "PR review completed"}

    return {"message": "Not a pull request or config event"}
