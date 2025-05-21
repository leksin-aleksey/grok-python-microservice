import requests

# My API Key
api_key = "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"

# Endpoint Groq
url = "https://api.groq.com/openai/v1/chat/completions"

# Body of the request
payload = {
    "model": "llama3-70b-8192",  # Одна из доступных моделей Groq
    "messages": [
        {"role": "user", "content": "Hi, could you send me the recipe of cocktails with beer?"}
    ],
    "temperature": 0.7
}

# Headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# sending request
response = requests.post(url, json=payload, headers=headers)

# Response answer
print(response.json()["choices"][0]["message"]["content"])
