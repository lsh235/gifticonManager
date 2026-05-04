from io import BytesIO

import pytesseract
from PIL import Image, ImageOps


def extract_text(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    gray = ImageOps.grayscale(image)
    bw = gray.point(lambda x: 0 if x < 160 else 255, mode="1")

    # kor + eng 혼합 문구 대응
    text = pytesseract.image_to_string(bw, lang="kor+eng")
    return text.strip()
