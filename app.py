import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

data = {
    "model": "qwen2.5:3b",
    "prompt": "Explain Node.js in simple terms",
    "stream": False
}

response = requests.post(OLLAMA_URL, json=data)
result = response.json()


print(result['response'])