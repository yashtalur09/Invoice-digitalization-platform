"""
CRUD operations for ExtractedFile model
"""
from sqlalchemy.orm import Session
try:
    from .models import ExtractedFile
except ImportError:
    from models import ExtractedFile
from typing import List, Optional
from datetime import datetime


def create_file(db: Session, user_id: int, file_name: str, content: str) -> ExtractedFile:
    """
    Create a new extracted file record in the database
    
    Args:
        db: Database session
        user_id: User identifier
        file_name: Name of the file
        content: Text content to store
        
    Returns:
        Created ExtractedFile object
    """
    db_file = ExtractedFile(
        user_id=user_id,
        file_name=file_name,
        content=content
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_file(db: Session, file_id: int) -> Optional[ExtractedFile]:
    """
    Get a file by its ID
    
    Args:
        db: Database session
        file_id: File identifier
        
    Returns:
        ExtractedFile object or None if not found
    """
    return db.query(ExtractedFile).filter(ExtractedFile.id == file_id).first()


def get_files_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[ExtractedFile]:
    """
    Get all files for a specific user
    
    Args:
        db: Database session
        user_id: User identifier
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of ExtractedFile objects
    """
    return db.query(ExtractedFile)\
        .filter(ExtractedFile.user_id == user_id)\
        .order_by(ExtractedFile.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


def delete_file(db: Session, file_id: int) -> bool:
    """
    Delete a file by its ID
    
    Args:
        db: Database session
        file_id: File identifier
        
    Returns:
        True if deleted, False if not found
    """
    db_file = db.query(ExtractedFile).filter(ExtractedFile.id == file_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
        return True
    return False

