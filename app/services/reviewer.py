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
                    "content": """You are a senior software engineer reviewing a pull request.
                - Analyze line-by-line
                - Mention specific line numbers
                - Highlight:
                * Code quality issues
                * Potential bugs
                * Security concerns
                - Use markdown formatting
                - Keep under 500 tokens"""
                },
                {
                    "role": "user",
                    "content": f"Please review this code diff:\n\n{diff_text}\n\n"
                           "Provide specific suggestions in bullet points. "
                           "If everything looks good, simply say 'LGTM (Looks Good To Me)'."
                }
            ],
            temperature=0.2,
            max_tokens=500
        )

        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "OpenAI review failed."


def review_with_deepseek(diff_text: str) -> str:
    """
    Correctly formatted request for DeepSeek's chat API
    """
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        messages = [
            {
                "role": "system",
                "content": """You are a senior software engineer reviewing a pull request.
                - Analyze line-by-line
                - Mention specific line numbers
                - Highlight:
                * Code quality issues
                * Potential bugs
                * Security concerns
                - Use markdown formatting
                - Keep under 500 tokens"""
            },
            {
                "role": "user",
                "content": f"Review this diff:\n```diff\n{diff_text}\n```"
            }
        ]

        payload = {
            "model": "deepseek-coder",  # Required field
            "messages": messages,  # Must use 'messages' not 'code'
            "temperature": 0.3,
            "max_tokens": 500,
            "stream": False  # Required by some APIs
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        # Detailed error reporting
        error_data = response.json()
        print(f"DeepSeek Error {response.status_code}: {error_data.get('message', 'No error details')}")
        return f"DeepSeek review failed (Status: {response.status_code})"

    except Exception as e:
        print(f"DeepSeek connection error: {str(e)}")
        return "DeepSeek review failed (Connection error)"
