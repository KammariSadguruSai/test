import streamlit as st
from utils.ocr import extract_text_from_image
from utils.tts import text_to_speech
from utils.scene_analysis import analyze_image
import os

# Configure Streamlit page
st.set_page_config(page_title="AI Assistive Tool", page_icon="👁️")

# File uploader widget
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file locally
    image_path = os.path.join("assets", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.image(image_path, caption="Uploaded Image", use_column_width=True)
    
    # Option for functionalities
    options = ["Scene Understanding", "Text-to-Speech", "Object Detection"]
    selected_option = st.selectbox("Select a functionality:", options)

    if selected_option == "Scene Understanding":
        st.subheader("Scene Description")
        description = analyze_image(image_path)
        st.write("\n".join(description))
    
    elif selected_option == "Text-to-Speech":
        st.subheader("Extracted Text to Speech")
        extracted_text = extract_text_from_image(image_path)
        st.write(extracted_text)
        
        if extracted_text:
            audio_path = text_to_speech(extracted_text)
            st.audio(audio_path, format="audio/mp3")
    
    elif selected_option == "Object Detection":
        st.subheader("Object Detection")
        objects = analyze_image(image_path)
        st.write("\n".join(objects))
