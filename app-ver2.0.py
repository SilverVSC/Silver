import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import plotly.express as px


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Silver AI Analyst Pro", page_icon="🧠")


if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Silver's Intelligent AI Analyst")
st.write("Now with memory! Chat with your data.")


uploaded_file = st.sidebar.file_uploader("Upload your CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File Loaded!")
    
   
    with st.expander("📊 View Data Table"):
        st.dataframe(df)
        st.subheader("📈 Data Visualization")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            
            fig_bar = px.bar(df, x='Name', y='Salary', title="Salaries by Employee", color='Department')
            st.plotly_chart(fig_bar, use_container_width=True)
        with v_col2:
            
            fig_pie = px.pie(df, names='Department', title="Department Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    if user_input := st.chat_input("Ask me about your data..."):
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

       
        data_context = df.to_string()
        
        
        try:
            with st.chat_message("assistant"):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": f"You are a professional data analyst. Use this data to answer: {data_context}"},
                        *st.session_state.messages 
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                
                
                st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV file from the sidebar to start the analysis.")