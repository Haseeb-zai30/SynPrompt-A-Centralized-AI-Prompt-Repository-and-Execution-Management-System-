import requests
from config import Config


def ask_ai(prompt, model):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    return f"Error: {response.json().get('error', {}).get('message', 'Unknown error')}"