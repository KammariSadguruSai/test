import streamlit as st
from PIL import Image
import pytesseract
import pyttsx3
from langchain.llms import GooglePalm
from langchain import PromptTemplate
from google.generativeai import configure

# Configure Google Generative AI
API_KEY = "AIzaSyBLlqhxWW1Bav8XqbvTwPFSGEwaoC1rASg"
configure(api_key=API_KEY)

# Streamlit application setup
st.set_page_config(page_title="AI Assistant for Visually Impaired")
st.title("AI-Powered Assistance for Visually Impaired Individuals")

# Upload image functionality
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Feature Selection
    selected_features = st.multiselect(
        "Select features to apply:",
        ["Real-Time Scene Understanding", "Text-to-Speech Conversion"],
    )

    if "Real-Time Scene Understanding" in selected_features:
        st.subheader("Real-Time Scene Understanding")
        # Google Generative AI for scene description
        llm = GooglePalm(model="text-bison-001", temperature=0.7)
        prompt = PromptTemplate(
            input_variables=["image_text"],
            template="Describe the content of the image: {image_text}",
        )
        extracted_text = pytesseract.image_to_string(image)
        scene_description = llm(prompt.format(image_text=extracted_text))
        st.write("Scene Description:")
        st.write(scene_description)

    if "Text-to-Speech Conversion" in selected_features:
        st.subheader("Text-to-Speech Conversion")
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image)
        st.write("Extracted Text:")
        st.write(extracted_text)

        # Convert extracted text to speech
        engine = pyttsx3.init()
        engine.say(extracted_text)
        engine.runAndWait()
        st.write("Speech output generated. (Audio will be heard locally)")

st.sidebar.info(
    """
    This application uses:
    - Google Generative AI for scene description.
    - OCR with pytesseract for text extraction.
    - pyttsx3 for text-to-speech conversion.
    """
)
