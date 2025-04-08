import openai
import requests
import os

# Make sure you set these environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

openai.api_key = OPENAI_API_KEY

def review_with_openai(diff_text: str) -> str:
    """
    Sends the diff to OpenAI's GPT-4o model for review.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior software engineer reviewing a pull request. "
                           "Provide concise, actionable feedback. Focus on:"
                           "\n- Code quality issues"
                           "\n- Potential bugs"
                           "\n- Security concerns"
                           "\n- Performance optimizations"
                           "\nKeep responses under 500 tokens."
                },
                {
                    "role": "user",
                    "content": f"Please review this code diff:\n\n{diff_text}\n\n"
                           "Provide specific suggestions in bullet points. "
                           "If everything looks good, simply say 'LGTM (Looks Good To Me)'."
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "OpenAI review failed."

def review_with_deepseek(diff_text: str) -> str:
    """
    Sends the diff to DeepSeek's API for code review (mocked or real).
    """
    try:
        url = "https://api.deepseek.com/v1/review"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        # Properly structured prompt with system message
        messages = [
            {
                "role": "system",
                "content": "You are a senior software engineer reviewing a pull request. "
                           "Provide concise, actionable feedback. Focus on:"
                           "\n- Code quality issues"
                           "\n- Potential bugs"
                           "\n- Security concerns"
                           "\n- Performance optimizations"
                           "\nKeep responses under 500 tokens."
            },
            {
                "role": "user",
                "content": f"Please review this code diff:\n\n{diff_text}\n\n"
                           "Provide specific suggestions in bullet points. "
                           "If everything looks good, simply say 'LGTM (Looks Good To Me)'."
            }
        ]

        payload = {
            "code": diff_text,
            "task": "code_review"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("review", "No review comment returned.")
        else:
            print(f"DeepSeek API error: {response.status_code}")
            return "DeepSeek review failed."
    except Exception as e:
        print(f"DeepSeek error: {e}")
        return "DeepSeek review failed."
