from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

engine = create_engine('sqlite:///databsae.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ItemsRepository:

    @staticmethod
    def get_items_by_user(user_id: str) -> List[Item]:
        db = SessionLocal()
        try:
            return db.query(Item).filter(Item.user_id == user_id).all()
        finally:
            db.close()

    @staticmethod
    def create_item(user_id: str, content: str) -> Item:
        db = SessionLocal()
        try:
            item = Item(user_id=user_id, content=content)
            db.add(item)
            db.commit()
            db.refresh(item)
            return item
        finally:
            db.close()
