from sqlalchemy.orm import Session
from app.models import Company, Employee
from app.schemas import EmployeeCreate
from typing import List
from sqlalchemy.exc import IntegrityError
from typing import List, Tuple, Set

def get_or_create_company(db: Session, name: str):
    company = db.query(Company).filter(Company.name == name).first()
    if not company:
        company = Company(name=name)
        db.add(company)
        db.commit()
        db.refresh(company)
    return company

def create_employees(db: Session, employees: List[EmployeeCreate], manager_ids: Set[int]):
    try:
        # First pass: Create all companies
        company_names = {e.company_name for e in employees}
        company_map = {}
        
        for name in company_names:
            company = db.query(Company).filter(Company.name == name).first()
            if not company:
                company = Company(name=name)
                db.add(company)
                db.commit()
                db.refresh(company)
            company_map[name] = company.id
        
        # Second pass: Create employees without managers first
        employee_map = {}
        non_manager_employees = []
        
        for emp in employees:
            if emp.manager_id is None or emp.manager_id not in manager_ids:
                db_emp = Employee(
                    first_name=emp.first_name,
                    last_name=emp.last_name,
                    phone_number=emp.phone_number,
                    salary=emp.salary,
                    manager_id=emp.manager_id,
                    department_id=emp.department_id,
                    company_id=company_map[emp.company_name]
                )
                non_manager_employees.append(db_emp)
        
        db.bulk_save_objects(non_manager_employees)
        db.commit()
        
        # Get IDs of newly created employees
        for emp in non_manager_employees:
            db.refresh(emp)
            employee_map[(emp.first_name, emp.last_name)] = emp.id
        
        # Third pass: Create employees with managers
        manager_employees = []
        
        for emp in employees:
            if emp.manager_id and emp.manager_id in manager_ids:
                # Check if manager exists in database
                manager_exists = db.query(Employee.id).filter(
                    Employee.id == emp.manager_id
                ).first()
                
                if not manager_exists:
                    raise ValueError(f"Manager ID {emp.manager_id} does not exist")
                
                db_emp = Employee(
                    first_name=emp.first_name,
                    last_name=emp.last_name,
                    phone_number=emp.phone_number,
                    salary=emp.salary,
                    manager_id=emp.manager_id,
                    department_id=emp.department_id,
                    company_id=company_map[emp.company_name]
                )
                manager_employees.append(db_emp)
        
        db.bulk_save_objects(manager_employees)
        db.commit()
        
        return len(non_manager_employees) + len(manager_employees)
        
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Database integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Unexpected error: {str(e)}")
    # First get all unique company names
    company_names = {e.company_name for e in employees}
    
    # Create company mapping (name -> id)
    company_map = {}
    for name in company_names:
        company = db.query(Company).filter(Company.name == name).first()
        if not company:
            company = Company(name=name)
            db.add(company)
            db.commit()
            db.refresh(company)
        company_map[name] = company.id
    
    # Prepare employee objects with proper company_id
    db_employees = []
    for employee in employees:
        db_employee = Employee(
            first_name=employee.first_name,
            last_name=employee.last_name,
            phone_number=employee.phone_number,
            salary=employee.salary,
            manager_id=employee.manager_id,
            department_id=employee.department_id,
            company_id=company_map[employee.company_name]
        )
        db_employees.append(db_employee)
    
    db.bulk_save_objects(db_employees)
    db.commit()
    return len(db_employees)