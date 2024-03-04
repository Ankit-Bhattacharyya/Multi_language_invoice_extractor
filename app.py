from dotenv import load_dotenv

load_dotenv() #Load all the environment variables from env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to load Gemini Pro Vishion
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,images,promt):
    response = model.generate_content([input,images[0],promt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, #get the mime type of the uploaded images
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
#Initilizing the gui of the app
st.set_page_config(page_title="Multi Language Invoice Extractor")

st.header("Multi Language Invoice Extractor")
input = st.text_input("Input promt : ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg","jpeg","png"])
image = ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.",  use_column_width=True)

submit = st.button("Tell me about the invoice")
input_promt = """You are an invoice expert. Images will be uploaded and you will get the answer according to the uploaded images"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input,image_data,input_promt)
    st.subheader("The response is")
    st.write(response)