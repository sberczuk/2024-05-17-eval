# db.py
from sqlmodel import SQLModel, create_engine
from models import Claim, ClaimLine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)