from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from pathlib import Path
from app.database import get_db
from app.utils.file_processor import process_employee_file
from app.crud import bulk_import_data
from app.schemas import ImportResult

router = APIRouter()

@router.post("/upload/", response_model=ImportResult)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Validate file type
        if not (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
            raise HTTPException(400, "Only .xlsx and .csv files are supported")
        
        # Save file temporarily
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        try:
            # Process file
            company_data, employee_data = process_employee_file(str(file_path))
            
            # Import data
            count = bulk_import_data(db, company_data, employee_data)
            
            return ImportResult(
                filename=file.filename,
                employee_count=count,
                status="success"
            )
        except Exception as e:
            raise HTTPException(422, detail=str(e))
        finally:
            if file_path.exists():
                os.unlink(file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")