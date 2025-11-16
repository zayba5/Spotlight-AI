import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
	DATABASE_URL,
	pool_pre_ping=True,
	future=True,
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True))
Base = declarative_base()


def get_db():
	"""
	Yield a database session tied to the current request context.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()



