import requests
import os

# # API Key from environment variable
# api_key = os.environ['grok_token']
#
# # Endpoint Groq
# url = "https://api.groq.com/openai/v1/chat/completions"
#
#
# def grok_question(question: str) -> str:
#      input("Write your question, please: ")
#
#
#     # Body of the request
#     payload = {
#         "model": "llama3-70b-8192",  # Одна из доступных моделей Groq
#         "messages": [
#             {"role": "user", "content": {}}
#         ],
#         "temperature": 0.7
#     }
#
#     # Headers
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#
#     # sending request
#     response = requests.post(url, json=payload, headers=headers)
#
#     # Response answer
#     print(response.json()["choices"][0]["message"]["content"])


def grok_question(question: str) -> str:
    # API Key from environment variable
    api_key = os.environ['grok_token']

    # Endpoint Groq
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Body of the request
    payload = {
        "model": "llama3-70b-8192",  # Одна из доступных моделей Groq
        "messages": [
            {"role": "user", "content": question}
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


