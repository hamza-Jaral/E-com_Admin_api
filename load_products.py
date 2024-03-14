import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import SQLALCHEMY_DATABASE_URL
from db.models.db_metadata import get_base
from db.models.product import Category, Product, Size

Base = get_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Load data from products.csv
try:
    products_df = pd.read_csv("products_data.csv")
except Exception as e:
    print(f"Error loading products.csv: {e}")
    exit(1)

# Data cleaning
print(f"Record Count before data cleaning: {len(products_df)}")
products_df = products_df.dropna(subset=["SKU_Code", "Design_No"])
products_df = products_df[products_df["SKU_Code"] != "#REF!"]
products_df = products_df.drop_duplicates(subset=["SKU_Code"])
print(f"Count after data cleaning: {len(products_df)}")


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
# Populate Product table

sum = 0
for index, row in products_df.iterrows():
    category = session.query(Category).filter_by(name=row["Category"]).first()
    size = session.query(Size).filter_by(name=row["Size"]).first()

    try:
        product = Product(
            sku_code=row["SKU_Code"],
            design_no=row["Design_No"],
            category=category,
            size=size,
        )
        session.add(product)
        session.commit()
        sum += 1

    except Exception as e:
        print(f"Error processing product '{row['SKU_Code']}': {e}")
        session.rollback()

print(f"{sum} Products inserted into DB")
# Close the session
session.close()

print("Data inserted successfully.")
