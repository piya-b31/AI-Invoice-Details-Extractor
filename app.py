from dotenv import load_dotenv 
load_dotenv()

import streamlit as st
import os 
from PIL import Image
from google import genai

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def get_gemini_response(input, image, prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",          # ← fixed model name
        contents=[input + "\n" + prompt, image]   
    )
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Handle PDF files
        if uploaded_file.type == "application/pdf":
            try:
                from pdf2image import convert_from_bytes
                pages = convert_from_bytes(uploaded_file.read())
                return pages[0]  # First page as image
            except Exception as e:
                st.error(f"Failed to convert PDF: {str(e)}")
                return None
        else:
            return Image.open(uploaded_file)
    else:
        st.warning("No file uploaded")
        return None


st.set_page_config(page_title="Multilanguage Details Extractor")
st.header("📃 Invoice Details Extractor")

input = st.text_input("Input Prompt", key="input")

uploaded_file = st.file_uploader(
    "Choose an image or PDF",
    type=["jpg", "jpeg", "png", "pdf"]   # ← added pdf
)

image = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        try:
            from pdf2image import convert_from_bytes
            uploaded_file.seek(0)  # reset file pointer
            pages = convert_from_bytes(uploaded_file.read())
            image = pages[0]
            st.image(image, caption="PDF Page 1 Preview", use_column_width=True)
        except Exception as e:
            st.error(f"Could not preview PDF: {str(e)}")
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("SUBMIT")

input_prompt = """
You are an expert in understanding bills. We will upload some image as bills and 
you have to answer any question based on the uploaded bill image. If you can't 
understand the image then say "Unable to understand the image". Answer based on 
the image only, not general knowledge. Answer in the same language as the input prompt.
Also if someone asks for summary of the bill, then give a summary of the bill in 3-4 lines. 
if something is not clear in the image, then say "Unable to understand that part of the image".
if the question is not related to the bill, then say "This question is not related to the bill".
"""

if submit:
    if input.strip() == "":
        st.warning("Input not provided (please enter a prompt)")
    else:
        image_data = input_image_setup(uploaded_file)
        if image_data:
            with st.spinner("Processing..."):
                response = get_gemini_response(input_prompt, image_data, input)
            st.subheader("Response")
            st.write(response)
