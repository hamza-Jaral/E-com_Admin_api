from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models.base_model import CreatedUpdatedAtModel
from db.models.db_metadata import get_base

Base = get_base()


class Order(CreatedUpdatedAtModel, Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="orders")
