from dotenv import load_dotenv 
load_dotenv()

import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image
from pypdf import PdfReader
from groq import Groq

# API Key
groq_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
groq_client = Groq(api_key=groq_key)

input_prompt = """
You are an expert in understanding bills, invoices, and financial documents.
You will be given either an image or extracted text from a bill/invoice.

Follow these rules strictly:
1. Answer ONLY based on the provided document content. No general knowledge.
2. If asked for a summary, provide a concise 3-4 line summary covering key details like vendor, amount, date, and items.
3. If any part is unclear or unreadable, say "Unable to understand that part of the document".
4. If the question is unrelated to the bill/invoice, say "This question is not related to the bill".
5. Do not add any extra information beyond what is asked.
6. Answer in the same language as the user's question.
7. If the document is completely unreadable or empty, say "Unable to understand the document".
"""


def setup_document(uploaded_file):
    if uploaded_file.type == "application/pdf":
        uploaded_file.seek(0)
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text, "pdf"
    else:
        uploaded_file.seek(0)
        return Image.open(uploaded_file), "image"


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def get_response(user_input, document, doc_type, chat_history):
    if doc_type == "pdf":
        # PDF → Groq LLaMA text model
        messages = [
            {
                "role": "system",
                "content": input_prompt + f"\n\nDocument Content:\n{document}"
            }
        ]
        for msg in chat_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        messages.append({
            "role": "user",
            "content": user_input
        })

        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return chat.choices[0].message.content

    else:
        # Image → Groq LLaMA 4 Scout (vision)
        try:
            img_base64 = image_to_base64(document)

            messages = [
                {
                    "role": "system",
                    "content": input_prompt
                }
            ]
            for msg in chat_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_input
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            })

            chat = groq_client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages
            )
            return chat.choices[0].message.content

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                return " Image analysis is not supported right now. Please try uploading a PDF or try again after some time."
            else:
                return f" Something went wrong: {error_str}"


# ─── UI ───────────────────────────────────────────────

st.set_page_config(page_title="Invoice Chatbot", page_icon="📃")
st.header("📃 Invoice Details Extractor")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document" not in st.session_state:
    st.session_state.document = None
if "doc_type" not in st.session_state:
    st.session_state.doc_type = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None

# File uploader
uploaded_file = st.file_uploader(
    "Upload your invoice (Image or PDF)",
    type=["jpg", "jpeg", "png", "pdf"]
)

if uploaded_file is not None:
    if st.session_state.file_name != uploaded_file.name:
        st.session_state.chat_history = []
        st.session_state.document, st.session_state.doc_type = setup_document(uploaded_file)
        st.session_state.file_name = uploaded_file.name

    if st.session_state.doc_type == "image":
        st.success(f"🖼️ Image uploaded: {uploaded_file.name}")
    else:
        st.info(f"📄 PDF uploaded: {uploaded_file.name}")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask anything about this invoice...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(
                    user_input,
                    st.session_state.document,
                    st.session_state.doc_type,
                    st.session_state.chat_history[:-1]
                )
                st.write(response)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

else:
    st.info("👆 Please upload an invoice image or PDF")
    st.session_state.chat_history = []
    st.session_state.document = None
    st.session_state.doc_type = None
    st.session_state.file_name = None
