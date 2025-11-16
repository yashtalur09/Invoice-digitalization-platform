"""
FastAPI Backend for OCR Dashboard
Main application file with all API endpoints
"""
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from pathlib import Path
import io

from database import get_db, init_db
from models import ExtractedFile
from crud import create_file, get_file, get_files_by_user
from ocr_service import ocr_service

# Initialize FastAPI app
app = FastAPI(title="OCR Dashboard API", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory if it doesn't exist
# Use parent directory for temp folder (project root)
TEMP_DIR = Path(__file__).parent.parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database on startup
    """
    init_db()
    print("Database initialized")


@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {"message": "OCR Dashboard API is running"}


@app.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    user_id: int = Form(1)  # Default user_id, can be changed later for auth
):
    """
    Process uploaded image and extract text using OCR
    
    Args:
        file: Uploaded image file
        user_id: User identifier (placeholder for now)
        
    Returns:
        Extracted text and metadata
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        file_extension = Path(file.filename).suffix
        temp_file_path = TEMP_DIR / f"upload_{user_id}_{file.filename}"
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        try:
            # Extract text using OCR service
            result = ocr_service.extract_text_from_image(str(temp_file_path))
            
            if not result['success']:
                raise HTTPException(status_code=500, detail=result.get('error', 'OCR processing failed'))
            
            return {
                "success": True,
                "text": result['text'],
                "word_count": result.get('word_count', 0),
                "message": "Text extracted successfully"
            }
        finally:
            # Clean up temporary file
            if temp_file_path.exists():
                temp_file_path.unlink()
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/save-text")
async def save_text(
    file_name: str = Form(...),
    text_content: str = Form(...),
    user_id: int = Form(1),  # Default user_id
    db: Session = Depends(get_db)
):
    """
    Save extracted text to PostgreSQL database
    
    Args:
        file_name: Name for the saved file
        text_content: Text content to save
        user_id: User identifier
        db: Database session
        
    Returns:
        Saved file information
    """
    try:
        # Validate inputs
        if not file_name.strip():
            raise HTTPException(status_code=400, detail="File name cannot be empty")
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="Text content cannot be empty")
        
        # Ensure file_name has .txt extension
        if not file_name.endswith('.txt'):
            file_name = file_name + '.txt'
        
        # Create file record in database
        db_file = create_file(
            db=db,
            user_id=user_id,
            file_name=file_name,
            content=text_content
        )
        
        return {
            "success": True,
            "file_id": db_file.id,
            "file_name": db_file.file_name,
            "created_at": db_file.created_at.isoformat(),
            "message": "File saved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


@app.get("/files/{user_id}")
async def get_files(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all saved files for a user
    
    Args:
        user_id: User identifier
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of saved files
    """
    try:
        files = get_files_by_user(db=db, user_id=user_id, skip=skip, limit=limit)
        
        return {
            "success": True,
            "files": [
                {
                    "id": file.id,
                    "file_name": file.file_name,
                    "created_at": file.created_at.isoformat(),
                    "content_length": len(file.content)
                }
                for file in files
            ],
            "total": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching files: {str(e)}")


@app.get("/download/{file_id}")
async def download_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    Download a saved text file from the database
    
    Args:
        file_id: File identifier
        db: Database session
        
    Returns:
        Text file as download response
    """
    try:
        db_file = get_file(db=db, file_id=file_id)
        
        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Create a file-like object from the text content
        file_content = io.BytesIO(db_file.content.encode('utf-8'))
        
        return StreamingResponse(
            io.BytesIO(db_file.content.encode('utf-8')),
            media_type="text/plain",
            headers={
                "Content-Disposition": f'attachment; filename="{db_file.file_name}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")


@app.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a saved file
    
    Args:
        file_id: File identifier
        db: Database session
        
    Returns:
        Success message
    """
    try:
        from crud import delete_file as crud_delete_file
        
        success = crud_delete_file(db=db, file_id=file_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="File not found")
        
        return {
            "success": True,
            "message": "File deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

