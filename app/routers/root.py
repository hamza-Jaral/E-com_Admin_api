from fastapi import APIRouter
from fastapi.responses import JSONResponse

app = APIRouter()


@app.get("/", response_class=JSONResponse, tags=["Root"])
def read_root():
    return {"message": "Welcome to the E-commerce Admin API"}
