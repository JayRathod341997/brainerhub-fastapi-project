import pandas as pd
from typing import List, Tuple, Set
from app.schemas import EmployeeCreate

def process_employee_file(file_path: str) -> Tuple[List[EmployeeCreate], Set[int]]:
    """Returns tuple of (employee_data, all_manager_ids)"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Collect all manager IDs referenced
        manager_ids = set()
        employees = []
        
        for _, row in df.iterrows():
            manager_id = int(row['MANAGER_ID']) if pd.notna(row['MANAGER_ID']) else None
            if manager_id:
                manager_ids.add(manager_id)
            
            employees.append(EmployeeCreate(
                first_name=str(row['FIRST_NAME']),
                last_name=str(row['LAST_NAME']),
                phone_number=str(row['PHONE_NUMBER']),
                salary=float(row['SALARY']),
                manager_id=manager_id,
                department_id=int(row['DEPARTMENT_ID']),
                company_name=str(row['COMPANY_NAME'])
            ))
        
        return employees, manager_ids
    except Exception as e:
        raise ValueError(f"File processing error: {str(e)}")