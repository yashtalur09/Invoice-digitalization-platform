"""
SQLAlchemy models for the OCR dashboard
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
try:
    from .database import Base
except ImportError:
    from database import Base


class ExtractedFile(Base):
    """
    Model for storing extracted text files in PostgreSQL
    """
    __tablename__ = "extracted_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  # Stores the .txt content
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ExtractedFile(id={self.id}, file_name='{self.file_name}', user_id={self.user_id})>"

