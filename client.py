#!/mnt/data/mikael/openai/bin/python3

import os
import json
from openai import OpenAI
import argparse
import readline

# Ensure to set your API key as an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to load messages from a JSON file
def load_messages(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading messages: {e}")
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
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        stream=True
    )

    full_response = ""

    for chunk in response:
        # Get the content from each streamed event
        content = chunk.choices[0].delta.content
        if type(content) is str:
            print(content, end="", flush=True)
            full_response += content

    print() # End with a newline

    return full_response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", default="gpt-3.5-turbo", help="language model to use")
    parser.add_argument("-i", "--input", help="input conversation file (JSON)")
    parser.add_argument("-o", "--output", help="output conversation file (JSON)")
    parser.add_argument("--io", help="mutable conversation file (JSON)")
    args = parser.parse_args()

    model_name = args.model
    if args.io:
        input_file = args.io
        output_file = args.io
    else:
        input_file = args.input
        output_file = args.output

    messages = []

    # If an input file is provided, load and replay messages
    if input_file:
        messages = load_messages(input_file)

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "user":
                 print("You: " + content)
            elif role == "assistant":
                 print("GPT: " + content)

        print()

    print("### Start chatting with GPT:")

    try:
        while True:
            user_input = input("You: ")

            # Append the user's input to the messages list
            messages.append({"role": "user", "content": user_input})

            # Get the assistant's response
            print("GPT: ", end="", flush=True)
            response_content = chat_with_gpt(messages, model_name)

            # Append the assistant's response to the messages list
            messages.append({"role": "assistant", "content": response_content})

    except KeyboardInterrupt:
        print("\nGoodbye! (Ctrl+C)")

    except EOFError:
        print("\nGoodbye! (Ctrl+D)")

    finally:
        # Save messages if an output file is provided
        if output_file:
            save_messages(messages, output_file)

if __name__ == "__main__":
    main()
