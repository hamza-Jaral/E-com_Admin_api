from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.inventory import Inventory as InventorySchema
from app.schemas.inventory import InventoryCreate
from db.database import get_db
from db.models.inventory import Inventory

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/", response_model=InventorySchema)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


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
    for key, value in inventory.dict().items():
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
