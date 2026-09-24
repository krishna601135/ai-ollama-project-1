from services.user_service import get_or_create_user
from services.conversation_service import create_conversation
from services.chat_service import save_message, ask_ollama


def main():

    # 1. Get/create user
    user = get_or_create_user(
        "mohan@example.com",
        "Mohan"
    )

    print("User:", user["name"])

    # 2. Create conversation
    conversation = create_conversation(
        user["_id"],
        "AI Chat"
    )

    conversation_id = conversation["_id"]

    print("Conversation created")
    print("Type 'exit' to quit")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        # 3. Save user message
        save_message(
            conversation_id,
            "user",
            user_input
        )

        # 4. Send conversation history to Ollama
        ask_ollama(conversation_id)


if __name__ == "__main__":
    main()