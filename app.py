from dotenv import load_dotenv 
load_dotenv()

import streamlit as st
import os 
from PIL import Image
from pypdf import PdfReader
from google import genai

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def get_gemini_response(input, image, prompt):
    if isinstance(image, str):
        contents = [input + "\n" + prompt + "\n\nDocument Content:\n" + image]
    else:
        contents = [input + "\n" + prompt, image]
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents
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
st.header("📃Invoice Details Extractor")
input = st.text_input("Input Prompt", key="input")
uploaded_file = st.file_uploader("Choose an image or PDF", type=["jpg", "jpeg", "png", "pdf"])

image = ""
if uploaded_file is not None:
    if uploaded_file.type != "application/pdf":
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        st.info("📄 PDF uploaded successfully!")

submit = st.button("SUBMIT")

input_prompt = """
You are an expert in understanding bills. We will upload some image as bills and you have to answer any question based on the uploaded bill image and if you can't understand the image then you have to say "Unable to understand the image". You have to answer based on the image and not based on any general knowledge. You have to answer in the same language as the input prompt.
"""

if submit:
    if input.strip() == "":
        st.warning("Input not provided (please enter a prompt)")
    else:
        uploaded_file.seek(0)
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        st.subheader("Response")
        st.write(response)
