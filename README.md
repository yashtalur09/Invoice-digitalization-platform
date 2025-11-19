# OCR Dashboard - Full Stack Application

A complete full-stack OCR (Optical Character Recognition) dashboard built with Python FastAPI backend, React frontend, and PostgreSQL database. This application allows users to upload images, extract text using OCR, preview the results, save them to the database, and download saved files.

##  Features

- **Image Upload**: Upload images for text extraction
- **OCR Processing**: Extract text from images using EasyOCR with advanced preprocessing
- **Text Preview**: View extracted text in a clean, formatted preview panel
- **Save to Database**: Save extracted text to PostgreSQL with custom file names
- **File Management**: List all saved files with metadata (name, date, size)
- **Download Files**: Download saved text files from the database
- **Modern UI**: Clean, responsive, and modern user interface

##  Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **EasyOCR**: OCR engine for text extraction
- **OpenCV**: Image preprocessing

### Frontend
- **React**: Frontend framework
- **Axios**: HTTP client for API calls
- **CSS3**: Modern styling with gradients and animations

##  Project Structure

```
Invoice-digitalization-platform/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and endpoints
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── crud.py              # CRUD operations
│   ├── ocr_service.py       # OCR integration service
│   └── init_db.py           # Database initialization script
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styles
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   └── package.json
├── script.py                # Original OCR script
├── requirements.txt         # Python dependencies
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14+ and npm
- PostgreSQL 12+ installed and running
- PostgreSQL database created

### Step 1: Database Setup

1. **Install PostgreSQL** (if not already installed)
   - Windows: Download from [PostgreSQL official website](https://www.postgresql.org/download/windows/)
   - macOS: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql`

2. **Create Database**
   ```sql
   CREATE DATABASE ocr_dashboard;
   ```

3. **Update Database Connection**
   - Edit `backend/database.py`
   - Update the `DATABASE_URL` with your PostgreSQL credentials:
   ```python
   DATABASE_URL = "postgresql://username:password@localhost:5432/ocr_dashboard"
   ```

### Step 2: Backend Setup

1. **Navigate to project directory**
   ```bash
   cd Invoice-digitalization-platform
   ```

2. **Create virtual environment** (if not already created)
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize Database**
   ```bash
   cd backend
   python init_db.py
   cd ..
   ```

6. **Start Backend Server**
   ```bash
   cd backend
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Step 3: Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

##  Usage

1. **Start Backend**: Make sure PostgreSQL is running and start the FastAPI server
2. **Start Frontend**: Start the React development server
3. **Open Browser**: Navigate to `http://localhost:3000`
4. **Upload Image**: Click "Choose Image File" and select an image
5. **Process**: Click "Process Image" to extract text
6. **Preview**: View the extracted text in the preview panel
7. **Save**: Enter a file name and click "Save to Database"
8. **Manage Files**: View, download, or delete saved files from the table

##  API Endpoints

### POST `/process-image`
Process an uploaded image and extract text.

**Request:**
- `file`: Image file (multipart/form-data)
- `user_id`: User identifier (form data, default: 1)

**Response:**
```json
{
  "success": true,
  "text": "Extracted text...",
  "word_count": 10,
  "message": "Text extracted successfully"
}
```

### POST `/save-text`
Save extracted text to the database.

**Request:**
- `file_name`: Name for the file (form data)
- `text_content`: Text content to save (form data)
- `user_id`: User identifier (form data)

**Response:**
```json
{
  "success": true,
  "file_id": 1,
  "file_name": "invoice_001.txt",
  "created_at": "2024-01-01T12:00:00",
  "message": "File saved successfully"
}
```

### GET `/files/{user_id}`
Get all saved files for a user.

**Response:**
```json
{
  "success": true,
  "files": [
    {
      "id": 1,
      "file_name": "invoice_001.txt",
      "created_at": "2024-01-01T12:00:00",
      "content_length": 150
    }
  ],
  "total": 1
}
```

### GET `/download/{file_id}`
Download a saved text file.

**Response:** Text file download

### DELETE `/files/{file_id}`
Delete a saved file.

**Response:**
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

## 🗄️ Database Schema

### `extracted_files` Table

| Column     | Type      | Description                    |
|------------|-----------|--------------------------------|
| id         | Integer   | Primary key                    |
| user_id    | Integer   | User identifier                |
| file_name  | String    | Name of the saved file         |
| content    | Text      | Text content (stored as .txt)  |
| created_at | DateTime  | Timestamp of creation          |

##  Configuration

### Environment Variables

You can set the database URL using an environment variable:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/ocr_dashboard"
```

### CORS Configuration

CORS is configured in `backend/main.py`. Update the `allow_origins` list if your frontend runs on a different port.

##  Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify database credentials in `backend/database.py`
- Check if the database exists: `psql -l`

### OCR Processing Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that image files are valid and readable
- First OCR run may take longer (downloading models)

### Frontend Connection Issues
- Verify backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Update `API_BASE_URL` in `frontend/src/App.js` if needed

##  Notes

- The OCR service initializes on first use and may take a moment
- Temporary uploaded files are automatically cleaned up after processing
- File names are automatically appended with `.txt` extension if not provided
- The application uses a placeholder `user_id` (1) - implement authentication for production

##  Production Deployment

For production deployment:

1. **Environment Variables**: Use environment variables for sensitive data
2. **Database**: Use a production PostgreSQL database
3. **Security**: Implement proper authentication and authorization
4. **CORS**: Configure CORS for your production domain
5. **Static Files**: Build React app: `npm run build` and serve with a web server
6. **Process Manager**: Use PM2 or similar for process management

##  License

This project is provided as-is for educational and development purposes.

##  Contributing

Feel free to submit issues and enhancement requests!

---

**Built with ❤️ using FastAPI, React, and PostgreSQL**
