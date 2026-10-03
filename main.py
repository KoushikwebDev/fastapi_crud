from fastapi import FastAPI, Depends
from models import Product, ProductSchema, APIResponse
from database import get_db, engine, Base
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World from FastAPI"}

# get products
@app.get("/products", response_model=APIResponse[list[ProductSchema]])
def read_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return APIResponse(
        status="success",
        message="Products retrieved successfully",
        data=products
    )

# add product
@app.post("/product", response_model=APIResponse[ProductSchema])
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    # here product is a pydantic model
    db_product = Product(**product.model_dump()) 
    # **product.model_dump() => **{'name': 'new name', 'description': 'new desc', 'price': 100.0, 'quantity': 10}
    # equivalent to => name='new name', description='new desc', price=100.0, quantity=10
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return APIResponse(
        status="success",
        message="Product created successfully",
        data=db_product
    )

