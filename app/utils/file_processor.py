import pandas as pd
from typing import Dict, List, Tuple
from app.schemas import EmployeeCreate

def process_employee_file(file_path: str) -> Tuple[List[Dict], List[Dict]]:
    """Returns (company_data, employee_data) as dictionaries ready for bulk insert"""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # Extract unique companies
    company_names = df['COMPANY_NAME'].unique()
    company_data = [{"name": name} for name in company_names]
    
    # Prepare employee data (manager_id handled later)
    employee_data = []
    for _, row in df.iterrows():
        employee_data.append({
            "first_name": str(row['FIRST_NAME']),
            "last_name": str(row['LAST_NAME']),
            "phone_number": str(row['PHONE_NUMBER']),
            "salary": float(row['SALARY']),
            "manager_id": int(row['MANAGER_ID']) if pd.notna(row['MANAGER_ID']) else None,
            "department_id": int(row['DEPARTMENT_ID']),
            "company_name": str(row['COMPANY_NAME'])
        })
    print(f"Processed {len(employee_data)} employees from {file_path}")
    return company_data, employee_data