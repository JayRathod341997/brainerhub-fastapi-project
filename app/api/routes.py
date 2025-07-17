from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from pathlib import Path
from app.schemas import ImportResult  # Add this import
from app import crud
from app.database import get_db
from app.utils.file_processor import process_employee_file

router = APIRouter()
@router.post("/upload/", response_model=ImportResult)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Validate file type
        if not (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
            raise HTTPException(
                status_code=400,
                detail="Only .xlsx and .csv files are supported"
            )
        
        # Save file temporarily
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        try:
            # Process file and get manager IDs
            employees, manager_ids = process_employee_file(str(file_path))
            
            # Import to database
            count = crud.create_employees(db, employees, manager_ids)
            
            return ImportResult(
                filename=file.filename,
                employee_count=count,
                status="success"
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        finally:
            if file_path.exists():
                file_path.unlink()
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )