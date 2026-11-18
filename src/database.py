
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL, SQL_DIR


def get_engine(url=None):
    """
    Create and return a SQLAlchemy database engine.
    Accepts a custom database URL for isolated testing.
    """
    url = url or DATABASE_URL

    if not url.startswith("sqlite"):
        raise ValueError(
            "This project currently supports SQLite."
        )

    return create_engine(
        url,
        future=True,
        connect_args={"check_same_thread": False}
    )


def initialize_database(engine=None):
    """
    Initialize database tables using schema.sql.
    """
    engine = engine or get_engine()

    schema_path = SQL_DIR / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")

    with engine.begin() as conn:
        for statement in schema.split(";"):
            if statement.strip():
                conn.execute(text(statement))

    return engine
