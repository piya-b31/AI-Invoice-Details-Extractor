
from dotenv import load_dotenv 
load_dotenv() #load all the environment variables from .env

import streamlit as st
import os 
from PIL import Image
from google import genai

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def get_gemini_response(input, image, prompt):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[input + "\n" + prompt, image]   
    )
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        return image   # return PIL image
    else:
        st.warning("No file uploaded")

st.set_page_config(page_title="Multilangauge Details Extractor")

st.header("📃Invoice Details Extractor")
input = st.text_input("Input Prompt", key = "input")
uploaded_file = st.file_uploader("Choose an image", type = ["jpg","jpeg","png","pdf"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Image", use_column_width=True)

submit = st.button("SUBMIT")

input_prompt = """
You are an expert in understanding bills. We will upload some image as bills and you have to answer any question based on the uploaded bill image and if you can't understand the image then you have to say "Unable to understand the image". You have to answer based on the image and not based on any general knowledge. You have to answer in the same language as the input prompt.
"""
#if submit button is clicked

if submit:
    if input.strip()=="":
        st.warning("Input not provided (please enter a prompt)")
    else:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)

        st.subheader("Response")
        st.write(response)   

