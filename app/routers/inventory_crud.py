from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.schemas.inventory import Inventory as InventorySchema
from app.schemas.inventory import InventoryCreate
from db.database import get_db
from db.models.inventory import Inventory

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/", response_model=InventorySchema)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    # Check if inventory already exists for the product
    existing_inventory = (
        db.query(Inventory).filter(Inventory.product_id == inventory.product_id).first()
    )
    if existing_inventory:
        raise HTTPException(
            status_code=400,
            detail="Inventory already exists for this product. Please update it instead.",
        )

    db_inventory = Inventory(**inventory.model_dump())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


@router.get("/", response_model=Page[InventorySchema])
def read_inventory(db: Session = Depends(get_db)):
    return paginate(db.query(Inventory).all())


@router.get("/{inventory_id}", response_model=InventorySchema)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory


@router.put("/{inventory_id}", response_model=InventorySchema)
def update_inventory(
    inventory_id: int, inventory: InventoryCreate, db: Session = Depends(get_db)
):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    for key, value in inventory.model_dump().items():
        setattr(db_inventory, key, value)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


@router.delete("/{inventory_id}")
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    db.delete(db_inventory)
    db.commit()
    return {"message": "Inventory deleted successfully"}


@router.get("/low_stock/", response_model=Page[InventorySchema])
def get_low_stock_inventory(threshold: int = 10, db: Session = Depends(get_db)):
    return paginate(
        db.query(Inventory).filter(Inventory.stock_quantity < threshold).all()
    )
