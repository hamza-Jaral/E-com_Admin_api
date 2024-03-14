from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from db.models.base_model import CreatedUpdatedAtModel
from db.models.db_metadata import get_base

Base = get_base()


class Category(CreatedUpdatedAtModel, Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), unique=True, index=True)

    products = relationship("Product", back_populates="category")


class Size(CreatedUpdatedAtModel, Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), unique=True, index=True)

    products = relationship("Product", back_populates="size")


class Product(CreatedUpdatedAtModel, Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku_code = Column(String(length=50), unique=True, index=True)
    design_no = Column(String(length=50), index=True)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2))

    # Relationships
    category_id = Column(Integer, ForeignKey("categories.id"))
    size_id = Column(Integer, ForeignKey("sizes.id"))

    category = relationship("Category", back_populates="products")
    size = relationship("Size", back_populates="products")
    orders = relationship("Order", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")
