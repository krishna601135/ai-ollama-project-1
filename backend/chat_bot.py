import requests
import json 

url = "http://localhost:11434/api/chat"

messages = [
#     {
#     "role": "system",
#     "content": "You are a Node.js teacher. Explain concepts simply and provide practical examples."
# }
]

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    data = {
        "model": "qwen2.5:3b",
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": 1.0,
            "num_predict": 100
        }
    }

    response = requests.post(url, json=data, stream=True)

    assistant_message = ""

    # result = response.json()

    # assistant_message = result["message"]["content"]

    # print("AI:", assistant_message)

    # messages.append({
    #     "role": "assistant",
    #     "content": assistant_message
    # })

    print("AI: ", end="", flush=True)

    for line in response.iter_lines():

        if line:
            chunk = json.loads(line)

            content = chunk["message"]["content"]

            print(content, end="", flush=True)

            assistant_message += content

    print()

    messages.append({
        "role": "assistant",
        "content": assistant_message
    })