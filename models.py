from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, Integer, String, Float

# ---------------------------------------------------------
# SQLAlchemy Model (Database Representation)
# ---------------------------------------------------------
# This model inherits from 'Base' and represents a table in our SQL database.
# SQLAlchemy uses this to create the table schema and perform database operations (queries, inserts).
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)

# ---------------------------------------------------------
# Pydantic Schema (Data Validation & API Serialization)
# ---------------------------------------------------------
# This schema is used by FastAPI to validate incoming request data and format
# outgoing response data (JSON). It does NOT interact directly with the database.
class ProductSchema(BaseModel):
    id: Optional[int] = None
    name : str
    description : str
    price : float
    quantity : int

    class Config:
        # Pydantic normally expects a dictionary. Since SQLAlchemy returns an ORM class object,
        # 'from_attributes = True' tells Pydantic to read the object's properties (e.g., product.name)
        # instead of a dictionary key (e.g., product["name"]).
        from_attributes = True

# ---------------------------------------------------------
# Generic Standardized API Response
# ---------------------------------------------------------
T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None