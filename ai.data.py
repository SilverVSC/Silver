import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role":"system",
            "content":"what is better for rdr2"
        },
        {
            "role":"user",
            "content":"3080 or 4060 ti"
        }

    ]
)
print(response.choices[0].message.content)