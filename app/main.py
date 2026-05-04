import json
from pathlib import Path

from fastapi import Depends, FastAPI, File, UploadFile
from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine
from .models import Gifticon
from .ocr import extract_text
from .parser import parse_dates

app = FastAPI(title="Gifticon Manager")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/gifticons")
async def create_gifticon(image: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await image.read()
    image_path = UPLOAD_DIR / image.filename
    image_path.write_bytes(content)

    raw_text = extract_text(content)
    dates = parse_dates(raw_text)

    row = Gifticon(
        image_path=str(image_path),
        raw_text=raw_text,
        parsed_dates=json.dumps(dates, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return {"id": row.id, "raw_text": raw_text, "parsed_dates": dates}
