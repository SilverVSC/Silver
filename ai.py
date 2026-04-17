import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("--- 🤖 Welcome to your AI Language Tutor ---")
user_input = input("Enter a sentence to check (English or German): ")

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": "You are a professional language tutor. Check grammar and spelling. Provide corrected version and brief explanation in English using bullet points."
            },
            {
                "role": "user", 
                "content": user_input
            }
        ]
    )
    print("\n--- 📝 Feedback ---")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"❌ Something went wrong: {e}")