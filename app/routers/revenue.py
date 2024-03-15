from datetime import datetime, timedelta
from typing import Dict, List, Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.order import Order as OrderSchema
from db.database import get_db
from db.models.product import Product
from db.models.sale import Order

router = APIRouter(tags=["analytics"])


class RevenueAnalysisResult(BaseModel):
    start_date: datetime
    end_date: datetime
    total_revenue: float


# Define the response model to return a list of revenue analysis results
class RevenueAnalysisResponse(BaseModel):
    revenue_results: List[RevenueAnalysisResult]


@router.get("/revenue", response_model=RevenueAnalysisResponse)
def analyze_revenue(
    start_date: datetime,
    end_date: datetime,
    analysis_period: str = Query(
        ..., description="Analysis period: daily, weekly, monthly, yearly"
    ),
    db: Session = Depends(get_db),
):
    revenue_results = []
    if analysis_period == "daily":
        current_date = start_date
        while current_date <= end_date:
            daily_revenue = (
                db.query(func.sum(Order.amount))
                .filter(Order.sale_date == current_date)
                .scalar()
                or 0
            )
            revenue_results.append(
                RevenueAnalysisResult(
                    start_date=current_date,
                    end_date=current_date,
                    total_revenue=daily_revenue,
                )
            )
            current_date += timedelta(days=1)
    elif analysis_period == "weekly":
        current_date = start_date
        while current_date <= end_date:
            weekly_end_date = current_date + timedelta(days=6)
            weekly_revenue = (
                db.query(func.sum(Order.amount))
                .filter(
                    Order.sale_date >= current_date, Order.sale_date <= weekly_end_date
                )
                .scalar()
                or 0
            )
            revenue_results.append(
                RevenueAnalysisResult(
                    start_date=current_date,
                    end_date=weekly_end_date,
                    total_revenue=weekly_revenue,
                )
            )
            current_date += timedelta(days=7)
    elif analysis_period == "monthly":
        current_date = start_date.replace(day=1)
        while current_date <= end_date:
            next_month_date = current_date + relativedelta(months=1) - timedelta(days=1)
            monthly_revenue = (
                db.query(func.sum(Order.amount))
                .filter(
                    Order.sale_date >= current_date, Order.sale_date <= next_month_date
                )
                .scalar()
                or 0
            )
            revenue_results.append(
                RevenueAnalysisResult(
                    start_date=current_date,
                    end_date=next_month_date,
                    total_revenue=monthly_revenue,
                )
            )
            current_date = next_month_date + timedelta(days=1)
    elif analysis_period == "yearly":
        current_date = start_date.replace(month=1, day=1)
        while current_date <= end_date:
            next_year_date = current_date + relativedelta(years=1) - timedelta(days=1)
            yearly_revenue = (
                db.query(func.sum(Order.amount))
                .filter(
                    Order.sale_date >= current_date, Order.sale_date <= next_year_date
                )
                .scalar()
                or 0
            )
            revenue_results.append(
                RevenueAnalysisResult(
                    start_date=current_date,
                    end_date=next_year_date,
                    total_revenue=yearly_revenue,
                )
            )
            current_date = next_year_date + timedelta(days=1)
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid analysis_period. Allowed values: daily, weekly, monthly, yearly",
        )

    return RevenueAnalysisResponse(revenue_results=revenue_results)


@router.get("/revenue/compare", response_model=Dict[str, float])
def compare_revenue(
    start_date: datetime,
    end_date: datetime,
    category_ids: List[int] = Query(..., description="List of category IDs"),
    db: Session = Depends(get_db),
):
    revenue_comparison = {}
    for category_id in category_ids:
        total_revenue = (
            db.query(func.sum(Order.amount))
            .filter(
                Order.sale_date >= start_date,
                Order.sale_date <= end_date,
                Order.product_id.in_(
                    db.query(Product.id).filter(Product.category_id == category_id)
                ),
            )
            .scalar()
            or 0
        )
        revenue_comparison[str(category_id)] = total_revenue
    return revenue_comparison


@router.get("/filter", response_model=Page[OrderSchema])
def filter_sales(
    start_date: datetime,
    end_date: datetime,
    product_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Order).filter(
        Order.sale_date >= start_date, Order.sale_date <= end_date
    )
    if product_id:
        query = query.filter(Order.product_id == product_id)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return paginate(query.all())
