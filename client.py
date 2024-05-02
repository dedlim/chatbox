#!/mnt/data/mikael/openai/bin/python3

import os
import json
from openai import OpenAI
import sys

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

def chat_with_gpt(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return response.choices[0].message.content

def main(input_file=None, output_file=None):
    global messages  # Declare messages as a global variable to modify it inside the function

    # Load messages if an input file is provided
    messages = load_messages(input_file) if input_file else []

    print("Start chatting with GPT (type 'exit' to stop):")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")

            # Save messages if an output file is provided
            if output_file:
                save_messages(messages, output_file)
            
            break

        # Append the user's input to the messages list
        messages.append({"role": "user", "content": user_input})

        # Get the assistant's response
        response_content = chat_with_gpt(messages)

        # Append the assistant's response to the messages list
        messages.append({"role": "assistant", "content": response_content})

        print("GPT: " + response_content)

if __name__ == "__main__":
    # Parse command line arguments for input and output files
    input_file = None
    output_file = None

    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if arg == "--in" and i + 1 < len(sys.argv):
                input_file = sys.argv[i + 1]
            elif arg == "--out" and i + 1 < len(sys.argv):
                output_file = sys.argv[i + 1]

    main(input_file, output_file)
