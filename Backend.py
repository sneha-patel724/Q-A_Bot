import tempfile
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI


# 🎯 Answer styles
LENGTH_INSTRUCTIONS = {
    "very_short": "Answer in 1 sentence only.",
    "short": "Answer in 2-3 sentences.",
    "long": "Answer in detailed explanation."
}


# 📄 Load PDF and return full text
def load_pdf(upload_file):
    suffix = Path(upload_file.name).suffix.lower()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(upload_file.getbuffer())
    tmp_path = tmp.name
    tmp.close()

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    full_text = "\n".join([doc.page_content for doc in docs])
    return full_text


# 🤖 Ask question using Gemini
def ask_question(question, document_text, api_key, length_mode):

    length_instruction = LENGTH_INSTRUCTIONS[length_mode]

    prompt = f"""
You are a document-based question answering assistant.

Rules:
- Answer ONLY from the document below
- Do NOT make up answers
- If not found, say:
  "This information is not in the document."

Answer style:
{length_instruction}

Document:
{document_text[:12000]}

Question:
{question}

Answer:
"""

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    response = llm.invoke(prompt)

    return response.content

