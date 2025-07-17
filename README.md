# FastAPI Excel Import

A FastAPI application for importing Excel/CSV data into a database.

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn app.main:app --reload`

## Features

- Upload Excel files with employee/company data
- Bulk insert into database
- Data validation with Pydantic models