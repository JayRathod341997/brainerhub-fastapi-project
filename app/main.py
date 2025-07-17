from fastapi import FastAPI
from app.database import engine, Base
from app.api.routes import router as api_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Excel/CSV to PostgreSQL Importer"}