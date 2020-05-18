"""
This holds our sqlalchemy database models

Note:
    - sqlite3 better for smaller number of users
        -lists in sqlite3: https://stackoverflow.com/questions/18708050/bulk-insert-list-values-with-sqlalchemy-core
    - MySql better for larger number of users
        -lists in MySql: https://stackoverflow.com/questions/8316176/insert-list-into-my-database-using-python
"""

from sqlalchemy import create_engine, Column, Text
from sqlalchemy.ext.declarative import declarative_base

Engine = create_engine("sqlite:///data.db")
Base = declarative_base(bind=Engine)


class Recipes(Base):
    """
    sqlalchemy recipes table
    """
    __tablename__ = 'recipes'

    ingredients = Column(Text, primary_key=True)
    ar_recipe_url = Column(Text)
    ar_recipe_name = Column(Text)
    fn_recipe_url = Column(Text)
    fn_recipe_name = Column(Text)
    ep_recipe_url = Column(Text)
    ep_recipe_name = Column(Text)


if __name__ == '__main__':
    Base.metadata.create_all(Engine)
