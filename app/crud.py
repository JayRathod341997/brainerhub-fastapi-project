from sqlalchemy.orm import Session
from app.models import Company, Employee
from app.schemas import EmployeeCreate
from typing import List, Dict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

def bulk_import_data(db: Session, company_data: List[Dict], employee_data: List[Dict]):
    # Start transaction
    transaction = db.begin()
    
    try:
        # Bulk insert companies
        if company_data:
            db.execute(
                text("""
                    INSERT INTO companies (name)
                    VALUES (:name)
                    ON CONFLICT (name) DO NOTHING
                """),
                company_data
            )
            db.flush()  # Ensure companies are available for querying
        
        # Get company name to ID mapping
        company_names = tuple({e['company_name'] for e in employee_data})
        result = db.execute(
            text("SELECT id, name FROM companies WHERE name IN :names"),
            {"names": company_names}
        ).fetchall()
        
        # Convert result to proper dictionary
        company_map = {name: id for id, name in result}
        
        # Prepare final employee data
        final_employee_data = []
        for emp in employee_data:
            company_id = company_map.get(emp['company_name'])
            if not company_id:
                raise ValueError(f"Company {emp['company_name']} not found")
            
            final_employee_data.append({
                "first_name": emp["first_name"],
                "last_name": emp["last_name"],
                "phone_number": emp["phone_number"],
                "salary": emp["salary"],
                "manager_id": emp["manager_id"],
                "department_id": emp["department_id"],
                "company_id": company_id
            })
        
        # Bulk insert employees
        if final_employee_data:
            db.execute(
                text("""
                    INSERT INTO employees 
                    (first_name, last_name, phone_number, salary, manager_id, department_id, company_id)
                    VALUES 
                    (:first_name, :last_name, :phone_number, :salary, :manager_id, :department_id, :company_id)
                """),
                final_employee_data
            )
        
        transaction.commit()
        return len(final_employee_data)
    
    except Exception as e:
        transaction.rollback()
        raise ValueError(f"Database operation failed: {str(e)}")
    # Start transaction
    transaction = db.begin()
    
    try:
        # Bulk insert companies and get their IDs
        if company_data:
            db.execute(
                text("""
                    INSERT INTO companies (name)
                    VALUES (:name)
                    ON CONFLICT (name) DO NOTHING
                """),
                company_data
            )
        
        # Get company name to ID mapping
        company_map = {c['name']: c['id'] for c in db.execute(
            text("SELECT id, name FROM companies WHERE name IN :names"),
            {"names": tuple({e['company_name'] for e in employee_data})}
        ).fetchall()}
        
        # Prepare final employee data with company IDs
        final_employee_data = []
        for emp in employee_data:
            final_emp = {
                "first_name": emp["first_name"],
                "last_name": emp["last_name"],
                "phone_number": emp["phone_number"],
                "salary": emp["salary"],
                "manager_id": emp["manager_id"],
                "department_id": emp["department_id"],
                "company_id": company_map[emp["company_name"]]
            }
            final_employee_data.append(final_emp)
        
        # Bulk insert employees
        if final_employee_data:
            db.execute(
                text("""
                    INSERT INTO employees 
                    (first_name, last_name, phone_number, salary, manager_id, department_id, company_id)
                    VALUES 
                    (:first_name, :last_name, :phone_number, :salary, :manager_id, :department_id, :company_id)
                """),
                final_employee_data
            )
        
        transaction.commit()
        return len(final_employee_data)
    
    except Exception as e:
        transaction.rollback()
        raise e