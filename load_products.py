import traceback
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import SQLALCHEMY_DATABASE_URL
from db.models import Order
from db.models.db_metadata import get_base
from db.models.inventory import Inventory
from db.models.product import Category, Product, Size

Base = get_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Load data from products.csv
try:
    products_df = pd.read_csv("products_data.csv")
except Exception as e:
    print(f"Error loading products.csv: {e}")
    exit(1)

try:
    sales_df = pd.read_csv("sales_data.csv")
except Exception as e:
    print(f"Error loading sales_data.csv: {e}")
    exit(1)

# Data cleaning
print(f"Record Count before data cleaning: {len(products_df)}")
products_df = products_df.dropna(subset=["SKU_Code", "Design_No", "Stock"])
products_df = products_df[products_df["SKU_Code"] != "#REF!"]
products_df = products_df.drop_duplicates(subset=["SKU_Code"])
print(f"Count after data cleaning: {len(products_df)}")

# Shuffle the rows in the products DataFrame
products_df = products_df.sample(frac=1, random_state=42).reset_index(drop=True)
# Limit the number of products to 1000
products_df = products_df.head(1000)
products_df["Description"] = (
    products_df["Category"]
    + " Size: "
    + products_df["Size"]
    + " Color: "
    + products_df["Color"]
)

# cleaning sales data

sales_df = sales_df.dropna()
sales_df = sales_df.rename(columns={"SKU": "SKU_Code"})
print("len of sales before cleaning", len(sales_df))
sales_df["Date"] = pd.to_datetime(sales_df["DATE"], format="%m-%d-%y", errors="coerce")
# Drop rows with invalid dates
sales_df = sales_df.dropna()
print("len of sales after cleaning dates", len(sales_df))

merged_df = pd.merge(
    products_df, sales_df, how="left", left_on="SKU_Code", right_on="SKU_Code"
)
# Create a new column "price" in products_df and fill it with values from "GROSS AMT" column
products_df["Price"] = merged_df["RATE"]
products_df = products_df.dropna()

filtered_sales_df = sales_df[sales_df["SKU_Code"].isin(products_df["SKU_Code"])]
print("len of Filtered sales", len(filtered_sales_df))

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Populate Category and Size tables
for category_name in products_df["Category"].unique():
    category = Category(name=category_name)
    session.add(category)

for size_name in products_df["Size"].unique():
    size = Size(name=size_name)
    session.add(size)

# Commit the changes to the database
try:
    session.commit()
except Exception as e:
    print(f"Error committing changes to the database: {e}")
    session.rollback()
    exit(1)

total_products = 0
for index, row in products_df.iterrows():
    category = session.query(Category).filter_by(name=row["Category"]).first()
    size = session.query(Size).filter_by(name=row["Size"]).first()

    try:
        product = Product(
            sku_code=row["SKU_Code"],
            design_no=row["Design_No"],
            description=row["Description"],
            price=row["Price"],
            category=category,
            size=size,
        )
        session.add(product)

        session.commit()
        total_products += 1

    except Exception as e:
        traceback.print_exc()
        print(f"Error processing product '{row['SKU_Code']}': {e}")
        session.rollback()
        exit(1)

    try:
        inventory_entry = Inventory(
            product_id=product.id,
            stock_quantity=row["Stock"],
            last_updated=datetime.now(),
        )
        session.add(inventory_entry)
        session.commit()

    except Exception as e:
        traceback.print_exc()
        print(f"Error processing inventory '{row['stock']}': {e}")
        session.rollback()
        exit(1)


orders_count = 0

for index, row in filtered_sales_df.iterrows():
    try:
        # Query the Product table to get the product_id based on SKU_Code
        product = session.query(Product).filter_by(sku_code=row["SKU_Code"]).first()
        if not product:
            print(
                f"Product with SKU code '{row['SKU_Code']}' not found in database. Skipping..."
            )
            continue
        price = float(product.price)

        # Create Order object
        order = Order(
            product_id=product.id,
            quantity=row["PCS"],
            amount=(price * float(row["PCS"])),
            sale_date=datetime.strptime(row["DATE"], "%m-%d-%y"),
        )

        session.add(order)
        session.commit()
        orders_count += 1

    except Exception:
        session.rollback()
        print(traceback.print_exc())
        exit(1)
        # print(f"Error in Creating Order with product: {product.id} Skipping...")
        # print(e)
        #
        # continue

# Close the session
session.close()


print(f"{total_products} Products inserted into DB")
print(f"{orders_count} Orders inserted into DB")
print("Data inserted successfully.")
