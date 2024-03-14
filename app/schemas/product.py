from pydantic import BaseModel


class ProductBase(BaseModel):
    sku_code: str
    design_no: str


class ProductCreate(ProductBase):
    category_id: int
    size_id: int


class ProductUpdate(ProductBase):
    pass


class ProductInDBBase(ProductBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ProductInDB(ProductInDBBase):
    pass


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDB(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class Category(CategoryInDB):
    pass


class SizeBase(BaseModel):
    name: str


class SizeCreate(SizeBase):
    pass


class SizeUpdate(SizeBase):
    pass


class SizeInDB(SizeBase):
    id: int

    class Config:
        from_attributes = True


class Size(SizeInDB):
    pass


class Product(ProductInDBBase):
    category: Category
    size: Size
