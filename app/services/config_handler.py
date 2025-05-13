
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
        # Extract JSON
        json_start = comment_body.index("{")
        config_json = comment_body[json_start:]
        user_config = json.loads(config_json)

        # Parse fields
        raw_model = user_config.get("preferred_model")  # optional
        model = raw_model.lower() if isinstance(raw_model, str) else None
        focus = user_config.get("focus")
        strictness = user_config.get("strictness")

        # Validate mandatory field strictness
        errors = []
        if not isinstance(strictness, str) or strictness.lower() not in VALID_STRICTNESS:
            strictness = "medium"
        else:
            strictness = strictness.lower()

        # Handle optional focus
        if not isinstance(focus, list) or not focus:
            focus = list(VALID_FOCUS)
        else:
            invalid_focus = set(focus) - VALID_FOCUS
            if invalid_focus:
                errors.append(f"❌ Invalid `focus` keys: {invalid_focus}. Allowed: {', '.join(VALID_FOCUS)}.")

        # Validate optional model if provided
        if model is not None:
            if model not in VALID_MODELS:
                errors.append(f"❌ Invalid `preferred_model`: `{model}`. Use `gpt-4o` or `deepseek`.")

        if errors:
            post_review_comment(comments_url, "\n".join(errors), "DualReview ❗️")
            return

        # Save valid config
        CONFIG_CACHE[pr_url] = {
            "focus": focus,
            "strictness": strictness,
            "preferred_model": model
        }

        # Acknowledge success
        success_msg = f"✅ Configuration saved for this PR!\n\n- **Focus**: {', '.join(focus)}\n- **Strictness**: `{strictness}`"
        if model:
            success_msg += f"\n- **Model**: `{model}`"
        else:
            success_msg += "\n- **Model**: `both (default)`"
        success_msg += "\n\nYou can reconfigure anytime by commenting again."

        post_review_comment(comments_url, success_msg, "DualReview")

    except Exception as e:
        post_review_comment(
            comments_url,
            f"⚠️ Failed to parse config. Make sure it's valid JSON.\n\nError: `{str(e)}`",
            "DualReview"
        )
