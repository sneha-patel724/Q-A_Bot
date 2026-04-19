import streamlit as st
import os
from Backend import load_pdf, ask_question
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="PDF Q&A Chatbot", layout="wide")

st.title("📄 PDF Question Answer Chatbot")

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# Answer length
length_mode = st.selectbox(
    "Answer Length",
    ["very_short", "short", "long"]
)

# Session state
if "doc_text" not in st.session_state:
    st.session_state.doc_text = None

# Load PDF
if uploaded_file:
    # We check if api_key exists in the background
    if not api_key:
        st.error("API Key not found! Please set GOOGLE_API_KEY in your .env file.")
    else:
        if st.session_state.doc_text is None:
            with st.spinner("Reading PDF..."):
                st.session_state.doc_text = load_pdf(uploaded_file)
            st.success("PDF loaded successfully!")

# Ask question
question = st.text_input("Ask your question")

if st.button("Ask"):
    if not api_key:
        st.error("Missing API Key in Environment Variables.")
    elif not st.session_state.doc_text:
        st.warning("Please upload a PDF first.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(
                question,
                st.session_state.doc_text,
                api_key,
                length_mode
            )

        st.subheader("Answer")
        st.write(answer)
