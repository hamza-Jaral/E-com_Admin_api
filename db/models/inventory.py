from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.models import CreatedUpdatedAtModel
from db.models.db_metadata import get_base

Base = get_base()


class Inventory(CreatedUpdatedAtModel, Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="inventory")

    __table_args__ = (
        CheckConstraint(
            "stock_quantity >= 0", name="stock_quantity_positive"
        ),  # Ensure stock_quantity is non-negative
    )
