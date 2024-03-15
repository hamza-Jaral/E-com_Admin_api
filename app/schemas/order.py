from datetime import datetime

from pydantic import BaseModel


class OrderBase(BaseModel):
    product_id: int
    quantity: int
    amount: float
    sale_date: datetime


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True


class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime
