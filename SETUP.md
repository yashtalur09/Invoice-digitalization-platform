# Quick Setup Guide

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ and npm installed
- [ ] PostgreSQL installed and running
- [ ] PostgreSQL database created

## Step-by-Step Setup

### 1. Database Setup (5 minutes)

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE ocr_dashboard;

-- Exit psql
\q
```

**Update database connection** in `backend/database.py`:
```python
DATABASE_URL = "postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/ocr_dashboard"
```

### 2. Backend Setup (10 minutes)

```bash
# Navigate to project
cd Invoice-digitalization-platform

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
cd backend
python init_db.py
cd ..

# Start backend (from project root)
cd backend
python main.py
```

Backend will run on: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### 3. Frontend Setup (5 minutes)

```bash
# Open new terminal
cd Invoice-digitalization-platform/frontend

# Install dependencies
npm install

# Start frontend
npm start
```

Frontend will run on: `http://localhost:3000`

## Testing the Application

1. Open browser: `http://localhost:3000`
2. Click "Choose Image File" and select an image
3. Click "Process Image"
4. Wait for text extraction (may take 10-30 seconds on first run)
5. Review extracted text
6. Enter a file name (e.g., "test_invoice")
7. Click "Save to Database"
8. Check the "Saved Files" table
9. Click "Download" to download the file

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running: `pg_isready`
- Verify database credentials in `backend/database.py`
- Ensure all dependencies installed: `pip list`

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check browser console for errors
- Verify CORS settings in `backend/main.py`

### OCR not working
- First run downloads models (may take 5-10 minutes)
- Check internet connection
- Verify image file is valid

### Database errors
- Run `python backend/init_db.py` again
- Check PostgreSQL logs
- Verify database exists: `psql -l`

## Common Issues

**Import errors**: Make sure you're running from the correct directory
**Port already in use**: Change port in `main.py` or kill existing process
**Module not found**: Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

- Customize user authentication
- Add more OCR languages
- Implement file search/filter
- Add export to PDF/Word
- Deploy to production

