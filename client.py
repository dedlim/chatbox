#!/mnt/data/mikael/openai/bin/python3

import os
import openai

# Ensure to set your API key as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    
    return response['choices'][0]['message']['content']

def main():
    print("Start chatting with GPT (type 'exit' to stop):")
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        response = chat_with_gpt(user_input)
        print("GPT: " + response)

if __name__ == "__main__":
    main()
