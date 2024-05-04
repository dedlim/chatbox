#!/mnt/data/mikael/openai/bin/python3

import os
import json
from openai import OpenAI
import argparse
import readline

color1 = "\033[93m"
color2 = "\033[0m"

# Ensure to set your API key as an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to load messages from a JSON file
def load_messages(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Warning: can't open '"+file_path+"'")
        return []

# Function to save messages to a JSON file
def save_messages(messages, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(messages, file, indent=2)
    except Exception as e:
        print(f"Error saving messages: {e}")

# Run one completion call, stream the result to stdout and return it
def chat_with_gpt(messages, model):
    global color1, color2

    print(color1 + "GPT: ", end="", flush=True)

    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0.0,
        stream=True
    )

    full_response = ""

    for chunk in response:
        # Get the content from each streamed event
        content = chunk.choices[0].delta.content
        if type(content) is str:
            print(content, end="", flush=True)
            full_response += content

    print(color2)
    print()

    return full_response

def main():
    global color1, color2

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", default="gpt-3.5-turbo")
    parser.add_argument('chatlog', nargs='?')

    parser.parse_args()
    args = parser.parse_args()

    model_name = args.model
    chatlog = args.chatlog

    messages = []

    # If chatlog file is provided, load and replay messages
    if chatlog:
        messages = load_messages(chatlog)

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "user":
                 print("You: " + content + "\n")
            elif role == "assistant":
                 print(color1 + "GPT: " + content + color2 + "\n")

    print("### Start chatting with GPT:")

    try:
        while True:
            user_input = input("You: ")
            print()

            # Append the user's input to the messages list
            messages.append({"role": "user", "content": user_input})

            # Get the assistant's response
            response_content = chat_with_gpt(messages, model_name)

            # Append the assistant's response to the messages list
            messages.append({"role": "assistant", "content": response_content})

    except KeyboardInterrupt:
        print("\nGoodbye! (Ctrl+C)")

    except EOFError:
        print("\nGoodbye! (Ctrl+D)")

    finally:
        # Save messages if an output file is provided
        if chatlog:
            save_messages(messages, chatlog)

if __name__ == "__main__":
    main()
