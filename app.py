from dotenv import load_dotenv 
load_dotenv()

import streamlit as st
import os 
from PIL import Image
from pypdf import PdfReader
from google import genai
from groq import Groq

# API Keys
gemini_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# Clients
gemini_client = genai.Client(api_key=gemini_key)
groq_client = Groq(api_key=groq_key)


def get_response(input, image_or_text, prompt):
    if isinstance(image_or_text, str):
        # PDF text → use Groq (free, unlimited)
        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"{input}\n\nDocument Content:\n{image_or_text}"
                }
            ]
        )
        return chat.choices[0].message.content
    else:
        # Image → use Gemini (vision support)
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt + "\n" + input, image_or_text]
        )
        return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            uploaded_file.seek(0)
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        else:
            return Image.open(uploaded_file)
    else:
        st.warning("No file uploaded")


st.set_page_config(page_title="Multilanguage Details Extractor")
st.header("📃 Invoice Details Extractor")
input = st.text_input("Input Prompt", key="input")
uploaded_file = st.file_uploader(
    "Choose an image or PDF",
    type=["jpg", "jpeg", "png", "pdf"]
)

image = ""
if uploaded_file is not None:
    if uploaded_file.type != "application/pdf":
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        st.info("📄 PDF uploaded successfully!")

submit = st.button("SUBMIT")

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

if submit:
    if input.strip() == "":
        st.warning("Please enter an input prompt.")
    elif uploaded_file is None:
        st.warning("Please upload an image or PDF.")
    else:
        uploaded_file.seek(0)
        image_data = input_image_setup(uploaded_file)
        if image_data is not None:
            with st.spinner("Analyzing..."):
                try:
                    response = get_response(input_prompt, image_data, input)
                    st.subheader("Response")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
