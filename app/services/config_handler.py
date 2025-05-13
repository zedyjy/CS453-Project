import json
from app.services.github_integration import post_review_comment

# In-memory config store (keyed by PR API URL)
CONFIG_CACHE = {}

# Allowed values
VALID_MODELS = {"gpt-4o", "deepseek"}
VALID_FOCUS = {
    "security", "readability", "performance", "bug-risk",
    "maintainability", "test-coverage", "documentation", "best-practices"
}
VALID_STRICTNESS = {"low", "medium", "high"}


async def handle_config_comment(payload: dict):
    comment_body = payload["comment"]["body"]
    pr_url = payload["issue"]["pull_request"]["url"]  # API URL to identify PR
    comments_url = payload["issue"]["comments_url"]   # where to reply

    try:
        # Extract JSON from comment body
        json_start = comment_body.index("{")
        config_json = comment_body[json_start:]
        user_config = json.loads(config_json)

        # Extract fields
        model = user_config.get("preferred_model", "").lower()
        focus = set(user_config.get("focus", []))
        strictness = user_config.get("strictness", "").lower()

        # Validation
        errors = []
        if model not in VALID_MODELS:
            errors.append(f"❌ Invalid `preferred_model`: `{model}`. Use `gpt-4o` or `deepseek`.")
        if not focus.issubset(VALID_FOCUS):
            errors.append(f"❌ Invalid `focus`: {focus - VALID_FOCUS}. Allowed: {', '.join(VALID_FOCUS)}.")
        if strictness not in VALID_STRICTNESS:
            errors.append(f"❌ Invalid `strictness`: `{strictness}`. Use `low`, `medium`, or `high`.")

        if errors:
            post_review_comment(comments_url, "\n".join(errors), "DualReview ❗️")
            return

        # Save valid config
        CONFIG_CACHE[pr_url] = {
            "preferred_model": model,
            "focus": list(focus),
            "strictness": strictness
        }

        # Acknowledge success
        success_msg = f"""✅ Configuration saved for this PR!

- **Model**: `{model}`
- **Focus**: {', '.join(focus)}
- **Strictness**: `{strictness}`

You can reconfigure anytime by commenting again.
"""
        post_review_comment(comments_url, success_msg, "DualReview")

    except Exception as e:
        post_review_comment(comments_url, f"⚠️ Failed to parse config. Make sure it's valid JSON.\n\nError: `{str(e)}`", "DualReview")
