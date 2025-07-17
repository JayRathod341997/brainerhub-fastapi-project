from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base # Importing Base from the same module

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    employees = relationship("Employee", back_populates="company")