import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq

# إعداد الصفحة والبيئة
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Silver AI Analyst", page_icon="🤖")

st.title("🤖 Silver's AI Data Dashboard")
st.write("Hello Silver, the app is running!")
st.write("Upload your data and let the AI analyze it for you!")

# 1. جزء رفع الملفات
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # قراءة البيانات
    df = pd.read_csv(uploaded_file)
    
    # تقسيم الصفحة لنصفين
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Data Preview")
        st.dataframe(df)
    
    with col2:
        st.subheader("📈 Quick Stats")
        st.write(df.describe())

    # 2. زرار تحليل الذكاء الاصطناعي
    if st.button("Analyze with AI"):
        with st.spinner("AI is thinking..."):
            try:
                data_summary = df.to_string()
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a professional business consultant."},
                        {"role": "user", "content": f"Analyze this data and give me 3 key insights:\n{data_summary}"}
                    ]
                )
                st.success("Analysis Complete!")
                st.markdown(f"### 📝 AI Insights:\n{response.choices[0].message.content}")
            except Exception as e:
                st.error(f"Error: {e}")