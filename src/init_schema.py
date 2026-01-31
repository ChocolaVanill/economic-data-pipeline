"""Initialize database schema for the pipeline.

This module ensures the bronze schema and tables exist before ingestion runs.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def get_connection_string() -> str:
    """Build PostgreSQL connection string from environment variables."""
    load_dotenv()
    
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DB")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def ensure_schema():
    """Create bronze schema and tables if they don't exist.
    
    """
    engine = create_engine(get_connection_string())
    
    # Read DDL from file
    ddl_path = Path(__file__).parent.parent / "sql" / "ddl" / "01_bronze_schema.sql"
    
    # Fallback for Airflow container path
    if not ddl_path.exists():
        ddl_path = Path("/opt/airflow/pipeline/sql/ddl/01_bronze_schema.sql")
    
    if not ddl_path.exists():
        raise FileNotFoundError(f"DDL file not found at {ddl_path}")
    
    ddl_sql = ddl_path.read_text()
    
    with engine.begin() as conn:
        conn.execute(text(ddl_sql))
    
    print("✅ Bronze schema initialized successfully")


if __name__ == "__main__":
    ensure_schema()
