# Import libraries
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Initiate env file
load_dotenv()

# Main function
def get_engine():
    """Database connection"""
    conn_string = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

    return create_engine(conn_string, future=True)