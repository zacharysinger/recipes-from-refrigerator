"""
This holds our sqlalchemy database models
"""

from sqlalchemy import create_engine, Column, String, PrimaryKeyConstraint, CLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Engine = create_engine("sqlite:///data.db")
Base = declarative_base(bind=Engine)

SessionFactory = sessionmaker(bind=Engine)


class Recipes(Base):
    """
    sqlalchemy recipes table
    """
    __tablename__ = 'recipes'

    ingredients = Column(String(10000), primary_key=True)
    source = Column(String(20))
    url = Column(CLOB)

    __table_args__ = (
        PrimaryKeyConstraint('ingredients', 'source'), {}
    )


if __name__ == '__main__':
    Base.metadata.create_all(Engine)
