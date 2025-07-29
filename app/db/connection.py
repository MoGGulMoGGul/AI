# app/db/connection.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # .env에 이미 있음

engine = create_engine(DATABASE_URL, echo=True)  # echo=True로 SQL 쿼리 로그 출력
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
