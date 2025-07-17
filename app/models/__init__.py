# app/models/__init__.py
from app.database import Base

# Import all your models here to ensure they're registered
from .company import Company
from .employee import Employee

__all__ = ["Base", "Company", "Employee"]