import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()
client = OpenAI()

VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID")

st.set_page_config(page_title="Benefit Buddy", layout="wide")
st.title("🧑‍⚕️ Benefit Buddy — Medicare Advantage Plan Q&A")

query = st.text_area("Ask a question about your plans:", "Which plans include dental coverage and what’s the annual max?")

if st.button("Ask"):
    if not VECTOR_STORE_ID:
        st.error("VECTOR_STORE_ID not set. Please run setx VECTOR_STORE_ID 'vs_...' and restart.")
    else:
        with st.spinner("Searching your plan PDFs..."):
            resp = client.responses.create(
                model="gpt-4.1-mini",
                input=query,
                tools=[{
                    "type": "file_search",
                    "vector_store_ids": [VECTOR_STORE_ID],
                }],
            )
        st.subheader("Answer")
        st.write(resp.output_text)