import streamlit as st
from PIL import Image
import pyttsx3
from google.cloud import vision
from langchain.chat_models import ChatOpenAI

# Configure Google Cloud Vision API
st.set_page_config(page_title="AI Assistant for Visually Impaired", layout="wide")
st.title("AI Assistant for Visually Impaired")

# Set up TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Adjust speech rate
tts_engine.setProperty('volume', 0.9)  # Adjust volume

# Function for OCR using Google Vision API
def extract_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f"{response.error.message}")
    return response.text_annotations[0].description if response.text_annotations else ""

# Function for real-time scene understanding using LangChain and ChatGPT
def generate_scene_description(image_path):
    # For simplicity, describe the image contents based on extracted OCR
    ocr_text = extract_text_from_image(image_path)
    prompt = (
        "Describe the image and interpret its contents for a visually impaired person. "
        f"Extracted text from the image: '{ocr_text}'."
    )
    llm = ChatOpenAI(temperature=0.5)  # Using OpenAI GPT model
    return llm.generate([{"role": "user", "content": prompt}]).generations[0][0]['text']

# Function to play text as speech
def text_to_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Streamlit app interface
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    
    # Save the uploaded image temporarily
    image_path = "uploaded_image.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())

    # Scene Understanding
    st.header("Scene Understanding")
    try:
        scene_description = generate_scene_description(image_path)
        st.text_area("Generated Scene Description", scene_description, height=200)
        if st.button("Play Scene Description"):
            text_to_speech(scene_description)
    except Exception as e:
        st.error(f"Error in scene understanding: {e}")

    # Text Extraction and Text-to-Speech
    st.header("Text-to-Speech for Visual Content")
    try:
        extracted_text = extract_text_from_image(image_path)
        st.text_area("Extracted Text", extracted_text, height=200)
        if st.button("Play Extracted Text"):
            text_to_speech(extracted_text)
    except Exception as e:
        st.error(f"Error in text extraction: {e}")
