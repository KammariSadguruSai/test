import os
from google.cloud import vision

def analyze_image(image_path):
    """Analyze image using Google Vision API for description and objects."""
    client = vision.ImageAnnotatorClient()
    
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    # Detect objects in the image
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    result = []
    for object_ in objects:
        result.append(f"{object_.name} (confidence: {object_.score:.2f})")
    
    if not result:
        result.append("No objects detected.")

    return result
