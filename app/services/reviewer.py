import openai
import requests
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

openai.api_key = OPENAI_API_KEY

# Descriptions for strictness levels
STRICTNESS_DESCRIPTIONS = {
    "low": "only major issues (blockers or high-severity bugs)",
    "medium": "balanced review: key improvements and reasonable style guidance",
    "high": "strictest review: includes nitpicks, formatting, and minor style tips"
}


def review_with_openai(diff_text: str, focus: list, strictness: str) -> str:
    """
    Sends the diff to OpenAI's GPT-4o model for review with detailed strictness descriptions.
    """
    try:
        focus_text = ", ".join(focus)
        desc = STRICTNESS_DESCRIPTIONS.get(strictness.lower(), "balanced review")
        system_prompt = f"""You are an expert AI code reviewer.

            You will receive a Git diff from a pull request. Your task is to return a JSON response analyzing the diff with:

            1. A concise summary of what the PR changes and its impact (max 1 paragraph).
            At the end of this summary, explicitly include:
            - Focus areas applied in this review: {focus_text if focus else 'all categories'}
            - Strictness level used: {strictness.upper()} — {desc}

            2. A list of detailed line-by-line comments relevant to the selected focus areas.

            Rules:
            - If focus areas are specified, only include comments with categories that match one of the focus areas.
            - If no focus is provided, use any category from ['bug', 'performance', 'readability', 'security', 'style', 'documentation'].
            - Do not include lines that do not match the focus areas.

            Each comment must include:
            - file: the filename (or "unknown")
            - line: the line number
            - issue: short description of the problem
            - suggestion: improved code or fix (if possible)
            - category: selected from the allowed list
            - severity: one of ['low', 'medium', 'high', 'critical']
            - confidence: a float between 0 and 1

            Output a single valid JSON object like:

            {{
            "summary": "<overall_summary including focus and strictness>",
            "comments": [
                {{
                "file": "<filename>",
                "line": <line_number>,
                "issue": "<description>",
                "suggestion": "<suggested_fix_or_code>",
                "category": "<category from focus>",
                "severity": "<severity>",
                "confidence": <float>
                }}
            ]
            }}

            Use markdown in suggestions.
            """



        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                { "role": "system", "content": system_prompt },
                {
                    "role": "user",
                    "content": f"Review this code diff:\n\n{diff_text}"
                }
            ],
            temperature=0.2,
            max_tokens=1000
        )

        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "OpenAI review failed."


def review_with_deepseek(diff_text: str, focus: list, strictness: str) -> str:
    """
    Sends the diff to DeepSeek's chat API for review with detailed strictness descriptions.
    """
    try:
        focus_text = ", ".join(focus)
        desc = STRICTNESS_DESCRIPTIONS.get(strictness.lower(), "balanced review")
        system_prompt = f"""You are an expert AI code reviewer.

            You will receive a Git diff from a pull request. Your task is to return a JSON response analyzing the diff with:

            1. A concise summary of what the PR changes and its impact (max 1 paragraph).
            At the end of this summary, explicitly include:
            - Focus areas applied in this review: {focus_text if focus else 'all categories'}
            - Strictness level used: {strictness.upper()} — {desc}

            2. A list of detailed line-by-line comments relevant to the selected focus areas.

            Rules:
            - If focus areas are specified, only include comments with categories that match one of the focus areas.
            - If no focus is provided, use any category from ['bug', 'performance', 'readability', 'security', 'style', 'documentation'].
            - Do not include lines that do not match the focus areas.

            Each comment must include:
            - file: the filename (or "unknown")
            - line: the line number
            - issue: short description of the problem
            - suggestion: improved code or fix (if possible)
            - category: selected from the allowed list
            - severity: one of ['low', 'medium', 'high', 'critical']
            - confidence: a float between 0 and 1

            Output a single valid JSON object like:

            {{
            "summary": "<overall_summary including focus and strictness>",
            "comments": [
                {{
                "file": "<filename>",
                "line": <line_number>,
                "issue": "<description>",
                "suggestion": "<suggested_fix_or_code>",
                "category": "<category from focus>",
                "severity": "<severity>",
                "confidence": <float>
                }}
            ]
            }}

            Use markdown in suggestions.
            """

        payload = {
            "model": "deepseek-coder",
            "messages": [
                { "role": "system", "content": system_prompt },
                { "role": "user", "content": f"Review this diff:\n```diff\n{diff_text}\n```" }
            ],
            "temperature": 0.2,
            "max_tokens": 1000,
            "stream": False
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        error_data = response.json()
        print(f"DeepSeek Error {response.status_code}: {error_data.get('message', 'No error details')}")
        return f"DeepSeek review failed (Status: {response.status_code})"

    except Exception as e:
        print(f"DeepSeek connection error: {str(e)}")
        return "DeepSeek review failed (Connection error)"
