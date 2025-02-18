#-----------Imports---------------
from google.cloud import vision
import io
import os
from dotenv import load_dotenv

#-------- Load Environment Variables ------------
load_dotenv()  # Load .env file
json_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

#-------- Define Vision API Client (AFTER setting credentials) ------------
client = vision.ImageAnnotatorClient()


#--------- Detect Labels ----------
def detect_labels(image_path):
    """Detects labels in the given image using Google Vision API."""
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    vision_image = vision.Image(content=content)
    response = client.label_detection(image=vision_image)
    labels = response.label_annotations

    if not labels:
        print("❌ No labels detected.")
        return None

    # Select the most confident label
    best_label = labels[0].description
    print(f"🔍 Best detected label: {best_label}")
    return best_label


#--------- Detect Text --------------
def detect_text(image_path):
    """Extracts relevant text from an image using Google Vision OCR."""
    try:
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        vision_image = vision.Image(content=content)
        response = client.text_detection(image=vision_image)

        if response.error.message:
            print(f"❌ Vision API Error: {response.error.message}")
            return None

        texts = response.text_annotations
        if not texts:
            print("❌ No text detected.")
            return None

        detected_text = texts[0].description
        print(f"📖 Detected Text (Raw):\n {detected_text}")

        # 🔹 Filter text to keep only relevant words
        words = detected_text.split("\n")  # Split text by new lines
        keywords = [word for word in words if len(word) > 3 and not word.isdigit()]  # Ignore short words and numbers

        refined_text = " ".join(keywords[:5])  # Keep first 5 words
        print(f"🔍 Filtered Text: {refined_text}")
        return refined_text

    except Exception as e:
        print(f"⚠️ Error in detect_text: {str(e)}")
        return None
