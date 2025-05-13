# 5. User Manual

## 5.1. Overview

The GitHub Review Bot automates code reviews by integrating AI-powered analysis into your development workflow. Key features include:

- **Automated Code Reviews**: Leveraging AI models like GPT-4o and DeepSeek to generate review comments on pull requests.
- **Customizable Review Settings**: Allowing users to tailor the bot's behavior to their preferences.
- **Integration with GitHub Webhooks**: Enabling real-time responses to pull request events.

---

## 5.2. Setting Up the Review Bot

### 5.2.1. Clone the Repository

```bash
git clone https://github.com/zedyjy/CS453-Project.git
cd CS453-Project
```

### 5.2.2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5.2.3. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
GITHUB_TOKEN=your_github_personal_access_token
```

Replace the placeholders with your actual API keys and GitHub token.

### 5.2.4. Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Ensure that port `8000` is accessible from the internet or use a tunneling service like [ngrok](https://ngrok.com/):

```bash
ngrok http 8000
```

Note the HTTPS URL provided by ngrok; you'll use this in the next step.

---

## 5.3. Configuring GitHub Webhooks

To allow GitHub to communicate with your bot:

1. Navigate to your repository on GitHub.
2. Click on **Settings > Webhooks > Add webhook**.
3. Fill in the form:
   - **Payload URL**: `https://your-server.com/webhook` (replace with your server's URL).
   - **Content type**: `application/json`.
   - **Secret**: *(Optional)* Add a secret token for security.
   - **Which events would you like to trigger this webhook?**:
     - Select **Let me select individual events**.
     - Check **Pull requests**.
4. Click **Add webhook**.

For detailed instructions, refer to [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks).

---

## 5.4. Using the Review Bot Features

### 5.4.1. Automated Code Reviews

Once the bot is set up and the webhook is configured, it automatically performs code reviews on every new or updated pull request. It uses GPT-4o and DeepSeek models to analyze code changes and generate helpful review comments directly on the pull request thread.

### 5.4.2. Customizing Review Settings

Users can configure how the bot behaves by posting a specially formatted comment on the pull request. This allows contributors to customize:

- Which AI model to use (GPT-4o, DeepSeek, or both)
- What aspects of the code to focus on (e.g., security, readability, performance)
- How strict the review should be

#### Example Comment to Configure the Bot

```json
@DualReview configure
{
  "preferred_model": "gpt-4o",
  "focus": ["security", "performance"],
  "strictness": "high"
}
```

#### Supported Settings

**preferred_model**

- `"gpt-4o"` – Uses OpenAI's GPT-4o
- `"deepseek"` – Uses DeepSeek's model
- *(If omitted, both are used.)*

**focus**

Choose any of the following areas:

- `"security"`
- `"readability"`
- `"performance"`
- `"bug-risk"`
- `"maintainability"`
- `"test-coverage"`
- `"documentation"`
- `"best-practices"`

**strictness**

- `"low"` – Flags only major issues
- `"medium"` – Balanced, highlights key concerns
- `"high"` – Strict; includes minor issues, suggestions, and style tips

#### Re-configuring the Bot

You can update your preferences at any time by commenting again with a new configuration. Only the latest comment will be used.

### 5.4.3. Example Workflow

1. A user opens a pull request.
2. The bot runs and posts its initial review.
3. The user decides to customize the review by commenting:

```json
@DualReview configure
{
  "preferred_model": "deepseek",
  "focus": ["readability", "best-practices"],
  "strictness": "medium"
}
```

4. The bot re-evaluates the pull request using the new preferences and updates its comments.

---

## 5.5. Input & Output

- **Input**: Pull Request events triggered in your GitHub repository.
- **Output**: AI-generated code review comments posted directly on the PR.

---

## 5.6. Troubleshooting

**Bot not responding to PRs**:
- Ensure the webhook is correctly configured and active.
- Check server logs for any errors.

**Invalid API keys**:
- Verify that your API keys are correct and have the necessary permissions.

**Server not receiving requests**:
- Confirm that your server is publicly accessible.
- If using ngrok or similar, ensure the tunnel is active.

---

## 5.7. Additional Resources

- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
