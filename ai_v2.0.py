import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are a helpful AI Assistant expert in Business Systems and AI Engineering."

print("--- 🤖 Welcome to Silver AI Assistant ---")
print("(Type 'exit' to quit)")

while True:
    user_input = input("\n👤 You: ")
    
    if user_input.lower() in ['exit', 'quit', 'خروج']:
        print("Goodbye! Don't forget to push your code to GitHub! 😉")
        break

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        
        reply = response.choices[0].message.content
        print(f"\n--- 📝 AI Response ---\n{reply}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
