from sqlalchemy.orm import Session

from db.models.product import Category


def create_category(db: Session, name: str):
    db_category = Category(name=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, new_name: str):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db_category.name = new_name
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
