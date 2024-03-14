# Loading env variables

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.routers import inventory_crud, products_crud, root, sales_crud

load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.app)
app.include_router(products_crud.router, tags=["Products"])
app.include_router(inventory_crud.router)
app.include_router(sales_crud.router)

add_pagination(app)
