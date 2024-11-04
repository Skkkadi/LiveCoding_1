from src.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    restriction = Column(Boolean, nullable=False)


class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    product_ids = Column(String, nullable=True)
    total = Column(Integer, nullable=True)


class Sell(Base):
    __tablename__ = 'sells'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    basket_id = Column(String, nullable=True)
    total = Column(Integer, nullable=True)

