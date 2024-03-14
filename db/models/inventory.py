from sqlalchemy import Column, DateTime, ForeignKey, Integer

from db.models.db_metadata import get_base

Base = get_base()


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    stock_quantity = Column(Integer)
    change_date = Column(DateTime)
