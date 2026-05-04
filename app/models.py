from sqlalchemy import Column, Integer, Text

from .db import Base


class Gifticon(Base):
    __tablename__ = "gifticons"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(Text, nullable=False)
    raw_text = Column(Text, nullable=False)
    parsed_dates = Column(Text, nullable=False)  # comma-separated ISO dates
