import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
df = pd.read_csv('data.csv')
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

avg_salary = df['Salary'].mean()
it_staff = df[df['Department'] == 'IT']

print("--- 📊 Data Summary ---")
print(f"Average Salary: {avg_salary}")
print(f"IT Department Employees:\n{it_staff}")

analysis_prompt = f"Based on this data: {df.to_string()}, give me a strategic insight about salaries and performance."

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a business data analyst."},
        {"role": "user", "content": analysis_prompt}
    ]
)

print("\n--- 🤖 AI Insight ---")
print(response.choices[0].message.content)