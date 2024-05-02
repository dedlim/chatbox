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

def chat_with_gpt(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    # Initialize an empty string to store the complete response
    full_response = ""

    for chunk in response:
        # Get the content from each streamed event
        content = chunk.choices[0].delta.content
        if type(content) is str:
            print(content, end="", flush=True)  # Print and flush each chunk
            full_response += content  # Append each chunk to form the complete response

    print()  # Print a newline at the end

    return full_response

def main(input_file=None, output_file=None, model_name=None):
    global messages  # Declare messages as a global variable to modify it inside the function

    if not model_name:
        model_name = "gpt-3.5-turbo"

    # Load messages if an input file is provided
    messages = load_messages(input_file) if input_file else []

    print("Start chatting with GPT (type 'exit' to stop):")

    for message in messages:
        if message.get("role") == "user":
            print("You: "+message.get("content"))
        elif message.get("role") == "assistant":
            print("GPT: "+message.get("content"))

    try:
        while True:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

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
    # Parse command line arguments for input and output files
    input_file = None
    output_file = None
    model_name = None

    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if arg == "--in" and i + 1 < len(sys.argv):
                input_file = sys.argv[i + 1]
            elif arg == "--out" and i + 1 < len(sys.argv):
                output_file = sys.argv[i + 1]
            elif arg == "--model" and i + 1 < len(sys.argv):
                model_name = sys.argv[i + 1]

    main(input_file, output_file, model_name)
