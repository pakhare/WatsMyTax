from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite Database setup
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base class for the ORM models
Base = declarative_base()

# SQLAlchemy ORM model for the User table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    country = Column(String, nullable=False)
    preferences = Column(JSON)  # You can store JSON or a serialized dictionary here

    __table_args__ = (
        CheckConstraint("username <> ''", name="check_username_non_empty"),
        CheckConstraint("password_hash <> ''", name="check_password_hash_non_empty"),
        CheckConstraint("country <> ''", name="check_country_non_empty"),
    )


    def __repr__(self):
        return f"User(username={self.username}, country={self.country})"

# Create the database and tables
Base.metadata.create_all(bind=engine)

# SessionLocal class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
