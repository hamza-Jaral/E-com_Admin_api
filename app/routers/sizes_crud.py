from sqlalchemy.orm import Session

from db.models.product import Size


def create_size(db: Session, name: str):
    db_size = Size(name=name)
    db.add(db_size)
    db.commit()
    db.refresh(db_size)
    return db_size


def get_sizes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Size).offset(skip).limit(limit).all()


def update_size(db: Session, size_id: int, new_name: str):
    db_size = db.query(Size).filter(Size.id == size_id).first()
    if db_size:
        db_size.name = new_name
        db.commit()
        db.refresh(db_size)
    return db_size


def delete_size(db: Session, size_id: int):
    db_size = db.query(Size).filter(Size.id == size_id).first()
    if db_size:
        db.delete(db_size)
        db.commit()
    return db_size
