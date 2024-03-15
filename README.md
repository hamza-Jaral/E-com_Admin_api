# FastAPI: E-commerce Admin API

This API provides detailed insights into sales, revenue, and inventory status, as well as allow new product registration

## Installation

1. Clone the repository:

   ```bash
   git clone <https://github.com/hamza-Jaral/E-com_Admin_api.git>
   cd <project_directory>
   ```
2. Create and activate a virtual environment:

    ```python3 -m venv venv```

    ```source venv/bin/activate```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Database Setup

1. Initialize the database:

    ```bash
    alembic upgrade head
    ```
2. Load the data:
    ```bash
    python load_data.py
   ```

## Usage
1. Run the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```
2. Visit http://localhost:8000/docs in your browser to access the Swagger UI for API documentation.
