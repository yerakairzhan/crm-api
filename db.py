# Database configuration and session management

from sqlalchemy import create_engine, String, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment variable or default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/task_manager"
)

# Create SQLAlchemy engine
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, **engine_kwargs)

# UUID type with SQLite fallback + conversion
class GUID(TypeDecorator):
    # Platform-independent GUID type.


    impl = CHAR(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return str(value)
        return str(uuid.UUID(str(value)))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(str(value))


UUIDType = GUID()

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    # Dependency for getting database session

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Initialize database tables

    from src.models.users import User
    from src.models.tasks import Task
    from src.models.comments import Comment

    Base.metadata.create_all(bind=engine)
