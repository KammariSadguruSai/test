import streamlit as st
from PIL import Image
import torch  # For YOLO object detection
from langchain.chat_models import ChatOpenAI
import openai  # Replace with Google Generative AI API integration
import cv2
import numpy as np

# Configure OpenAI API Key (Replace with Google Generative AI API if available)
openai.api_key = "AIzaSyBSgtbnMK8b-lkuRQkD_WNYtrJaH2JmBPU"  # Add your API key

# Load Pre-trained YOLOv5 Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # YOLOv5 small model

# Streamlit App
st.title("AI-Powered Solution for Visually Impaired")
st.subheader("Upload an image for assistance")

# Image Upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display Uploaded Image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # ---- Real-Time Scene Understanding ----
    st.subheader("1. Real-Time Scene Understanding")
    with st.spinner("Analyzing the image..."):
        # Simulated API call using OpenAI's GPT (replace with Google Generative AI)
        image_caption = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Describe the scene in the uploaded image in detail.",
            max_tokens=100
        )["choices"][0]["text"].strip()
    st.write("**Generated Description:**", image_caption)

    # ---- Object and Obstacle Detection ----
    st.subheader("2. Object and Obstacle Detection")
    with st.spinner("Detecting objects and obstacles..."):
        # Convert PIL image to a format suitable for YOLOv5
        image_cv = np.array(image.convert("RGB"))
        results = model(image_cv)  # YOLO model inference
        detected_image = np.squeeze(results.render())  # Annotated image

        # Display Detected Objects
        st.image(detected_image, caption="Detected Objects", use_column_width=True)

        # List Detected Objects
        detected_objects = results.pandas().xyxy[0]["name"].tolist()
        st.write("**Detected Objects:**", ", ".join(detected_objects))

# Instructions to Install Required Libraries
st.sidebar.title("Requirements")
st.sidebar.write("""
To run this app, ensure you have the following libraries installed:
- `streamlit`
- `Pillow`
- `torch`
- `opencv-python`
- `langchain`
- `openai` or Google Generative AI equivalent
""")
