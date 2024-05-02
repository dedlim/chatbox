#!/mnt/data/mikael/openai/bin/python3

import os
from openai import OpenAI

# Ensure to set your API key as an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize an empty messages list to store the conversation context
messages = []

def chat_with_gpt(messages, model="gpt-4-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    # Return the content of the first choice
    return response.choices[0].message.content

def main():
    global messages  # Declare messages as a global variable to modify it inside the function

    print("Start chatting with GPT (type 'exit' to stop):")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Append the user's input to the messages list
        messages.append({"role": "user", "content": user_input})

        # Get the assistant's response
        response_content = chat_with_gpt(messages)

        # Append the assistant's response to the messages list
        messages.append({"role": "assistant", "content": response_content})

        print("GPT: " + response_content)

if __name__ == "__main__":
    main()
