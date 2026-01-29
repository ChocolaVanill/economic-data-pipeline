# Import libraries
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Initiate env file
load_dotenv()


# Main function
def get_engine() -> Engine:
    """Database connection"""
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    conn_string = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    return create_engine(conn_string, future=True)
