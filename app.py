import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import plotly.express as px

# 1. إعدادات البيئة والمفاتيح
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Silver AI Analyst Pro", page_icon="🧠")

# 2. تهيئة الذاكرة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Silver's Intelligent AI Analyst")
st.write("Now with memory! Chat with your data.")

# 3. رفع ملف البيانات
uploaded_file = st.sidebar.file_uploader("Upload your CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File Loaded!")
    
    # عرض البيانات في الجنب
    with st.expander("📊 View Data Table"):
        st.dataframe(df)
        st.subheader("📈 Data Visualization")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            # رسم بياني للأعمدة (رواتب الموظفين)
            fig_bar = px.bar(df, x='Name', y='Salary', title="Salaries by Employee", color='Department')
            st.plotly_chart(fig_bar, use_container_width=True)
        with v_col2:
            # رسم بياني دائري (توزيع الأقسام)
            fig_pie = px.pie(df, names='Department', title="Department Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

    # 4. عرض تاريخ المحادثة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. منطقة الشات (Chat Input)
    if user_input := st.chat_input("Ask me about your data..."):
        # إضافة رسالة المستخدم للذاكرة وعرضها
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # تحضير البيانات كإطار معرفي للـ AI
        data_context = df.to_string()
        
        # إرسال الطلب للـ AI مع سياق البيانات
        try:
            with st.chat_message("assistant"):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"You are a professional data analyst. Use this data to answer: {data_context}"},
                        *st.session_state.messages # إرسال تاريخ المحادثة بالكامل
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                
                # حفظ رد الـ AI في الذاكرة
                st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV file from the sidebar to start the analysis.")