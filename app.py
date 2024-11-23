import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import os
from io import BytesIO
from google.cloud import vision
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# Configure Google Generative AI (Vision API)
def google_vision_analysis(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as img_file:
        content = img_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    description = [label.description for label in labels]
    return description

# Scene Understanding using LangChain
def generate_scene_description(labels):
    openai_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["labels"],
        template="Using the following keywords {labels}, generate a description of the scene in detail."
    )
    chain = LLMChain(llm=openai_llm, prompt=prompt)
    return chain.run({"labels": labels})

# Text-to-Speech Conversion
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# OCR Extraction
def extract_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text.strip()

# Streamlit Application
def main():
    st.title("AI-Powered Assistance for Visually Impaired Individuals")
    st.subheader("Upload an image to use assistive functionalities.")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        # Save and display uploaded image
        image_path = f"temp_{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())
        image = Image.open(image_path)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Choose functionality
        st.sidebar.title("Select Feature")
        features = ["Real-Time Scene Understanding", "Text-to-Speech Conversion"]
        selected_feature = st.sidebar.radio("Choose a functionality", features)

        if selected_feature == "Real-Time Scene Understanding":
            st.header("Real-Time Scene Understanding")
            labels = google_vision_analysis(image_path)
            st.write("Detected Objects/Labels:", labels)

            scene_description = generate_scene_description(labels)
            st.write("Scene Description:")
            st.success(scene_description)

        elif selected_feature == "Text-to-Speech Conversion":
            st.header("Text-to-Speech Conversion")
            extracted_text = extract_text(image_path)
            if extracted_text:
                st.write("Extracted Text:")
                st.info(extracted_text)
                
                audio_file = text_to_speech(extracted_text)
                st.audio(audio_file, format="audio/mp3")
            else:
                st.error("No text found in the image.")

        # Clean up
        os.remove(image_path)

if __name__ == "__main__":
    main()
