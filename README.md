# Oil and Gas Dashboard

## Installation

1. Install conda environment

```
conda create --name vapourware python=3.11.5
```

2. Activate conda environment

```
conda activate vapourware
```

3. Install requirements

```
pip install -r requirements.txt
```

4. Connect with Database go to .env.example file and fill the variables
5. rename .env.example to .env
6. Run Alembric migrations

```
alembic upgrade head
```

7. Run the app

```
uvicorn main:app --reload
```

5. Open the app in your browser

```
http://localhost:8000/
```

#### Updates
1. Make the necessary changes to model
2. Generate an Alembic migration script using the following command:
```
$ poetry shell
> alembic revision --autogenerate -m <name_of_migration>
```
3. Apply the migration to update the database schema:
```
alembic upgrade head
```
4. Downgrade **(if necessary)** to a previous revision using the following command:
```
alembic downgrade <revision>
```
