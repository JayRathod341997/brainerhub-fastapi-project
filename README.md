# FastAPI Excel/CSV to PostgreSQL Importer

A high-performance API for bulk importing employee data from Excel/CSV files into PostgreSQL, maintaining company-employee relationships without using ORM queries in loops.

## Features

- **Bulk Data Import**: Processes thousands of records efficiently
- **File Support**: Handles both Excel (.xlsx) and CSV formats
- **Data Relationships**: Maintains company-employee relationships
- **Optimized Performance**: Uses raw SQL bulk operations
- **Validation**: Comprehensive data validation before import
- **Error Handling**: Detailed error reporting

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Poetry (recommended) or pip

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/JayRathod341997/brainerhub-fastapi-project.git
   cd brainerhub-fastapi-project

2. **Set up environment variables**
    ```bash
    DB_USER=postgres
    DB_PASSWORD=yourpassword
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=excel_import

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Database setup**
    ```bash
    createdb excel_import

5. **Running the API**
    ```bash
    uvicorn app.main:app --reload

