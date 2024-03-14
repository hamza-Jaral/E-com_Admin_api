from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.schemas.product import Product as ProductInDB
from app.schemas.product import ProductCreate, ProductUpdate
from db.database import get_db
from db.models.product import Product

router = APIRouter()


@router.post(
    "/products/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED
)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/products/", response_model=Page[ProductInDB])
async def read_products(db: Session = Depends(get_db)):
    return paginate(db.query(Product).all())


@router.get("/products/{product_id}", response_model=ProductInDB)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product


@router.put("/products/{product_id}", response_model=ProductUpdate)
async def update_product(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
):
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            for field, value in product_update.dict(exclude_unset=True).items():
                setattr(db_product, field, value)
            db.commit()
            db.refresh(db_product)
        return db_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/products/{product_id}")
async def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    raise HTTPException(status_code=404, detail="Product not found")
