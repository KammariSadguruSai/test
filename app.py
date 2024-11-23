import streamlit as st
from PIL import Image
import pyttsx3
import os
import pytesseract  
import google.generativeai as genai

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Google Generative AI with API Key
GEMINI_API_KEY = "AIzaSyBSgtbnMK8b-lkuRQkD_WNYtrJaH2JmBPU"  # Replace with your valid API key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# App Header
st.title("VisionAssist 👁")
st.subheader("AI for Scene Understanding, Text Extraction & Speech for the Visually Impaired")

# Sidebar
st.sidebar.title("ℹ About")
st.sidebar.write("""
- 🔍 Describe Scene: AI insights for image content.
- 📝 Extract Text: OCR-based text extraction.
- 🔊 Text-to-Speech: Hear the extracted text aloud.
""")

# Functions
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(prompt, image_data):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt, image_data])
    return response.text

# File Upload
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Features
col1, col2, col3 = st.columns(3)
if col1.button("🔍 Describe Scene") and uploaded_file:
    prompt = "Describe the scene in detail for a visually impaired person."
    image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
    st.write("Scene Description:", generate_scene_description(prompt, image_data))

if col2.button("📝 Extract Text") and uploaded_file:
    st.write("Extracted Text:", extract_text_from_image(image))

if col3.button("🔊 Text-to-Speech") and uploaded_file:
    text = extract_text_from_image(image)
    if text.strip():
        text_to_speech(text)
        st.success("✅ Speech Generated")
    else:
        st.warning("No text found!")

# Footer
st.sidebar.write("Powered by Google Gemini API | Built with ❤ using Streamlit")
