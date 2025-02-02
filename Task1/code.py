import sys
from PIL import Image
import pytesseract

def image_to_text(img_path):
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    assert(len(sys.argv) == 2)

    image_path = sys.argv[1].strip("\"")
    print(image_to_text(image_path))
