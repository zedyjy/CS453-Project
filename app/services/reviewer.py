import openai
import requests
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

openai.api_key = OPENAI_API_KEY

def review_with_openai(diff_text: str, focus: list, strictness: str) -> str:
    try:
        focus_text = ", ".join(focus)
        system_prompt = f"""You are a senior software engineer reviewing a pull request.

- Focus areas: {focus_text}
- Strictness level: {strictness.upper()}
- Analyze line-by-line
- Mention specific line numbers
- Highlight:
    * Code quality issues
    * Potential bugs
    * Security concerns
- Use markdown formatting
- If everything looks good, say 'LGTM'
- Keep your response under 500 tokens"""

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
            max_tokens=500
        )

        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "OpenAI review failed."


def review_with_deepseek(diff_text: str, focus: list, strictness: str) -> str:
    try:
        focus_text = ", ".join(focus)
        system_prompt = f"""You are a senior software engineer reviewing a pull request.

- Focus areas: {focus_text}
- Strictness level: {strictness.upper()}
- Analyze line-by-line
- Mention specific line numbers
- Highlight:
    * Code quality issues
    * Potential bugs
    * Security concerns
- Use markdown formatting
- If everything looks good, say 'LGTM'
- Keep your response under 500 tokens"""

        payload = {
            "model": "deepseek-coder",
            "messages": [
                { "role": "system", "content": system_prompt },
                { "role": "user", "content": f"Review this diff:\n```diff\n{diff_text}\n```" }
            ],
            "temperature": 0.2,
            "max_tokens": 500,
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
