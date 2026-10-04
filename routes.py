from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Product, ProductSchema, APIResponse

router = APIRouter(
    tags=["Products"]
)

# get products
@router.get("/products", response_model=APIResponse[list[ProductSchema]])
def read_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return APIResponse(
        status="success",
        message="Products retrieved successfully",
        data=products
    )

# search products (using query parameters)
# URL example: /products/search?name=apple&limit=5
@router.get("/products/search", response_model=APIResponse[list[ProductSchema]])
def search_products(name: str, limit: int = 10, db: Session = Depends(get_db)):
    # Using .ilike() for case-insensitive search
    products = db.query(Product).filter(Product.name.ilike(f"%{name}%")).limit(limit).all()
    return APIResponse(
        status="success",
        message=f"Search results for '{name}'",
        data=products
    )

# add product
@router.post("/product", response_model=APIResponse[ProductSchema])
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

# get product by id
@router.get("/product/{id}", response_model=APIResponse[ProductSchema])
def read_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        return APIResponse(
            status="error",
            message="Product not found",
            data=None
        )
    return APIResponse(
        status="success",
        message="Product retrieved successfully",
        data=product
    )

# update product
@router.put("/product", response_model=APIResponse[ProductSchema])
def update_product(product: ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product.id).first()
    if not db_product:
        return APIResponse(
            status="error",
            message="Product not found",
            data=None
        )
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product) 
    return APIResponse(
        status="success",
        message="Product updated successfully",
        data=db_product
    )

# delete product
@router.delete("/product/{id}", response_model=APIResponse[ProductSchema])
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        return APIResponse(
            status="error",
            message="Product not found",
            data=None
        )
    db.delete(db_product)
    db.commit()
    return APIResponse(
        status="success",
        message="Product deleted successfully",
        data=None
    )
