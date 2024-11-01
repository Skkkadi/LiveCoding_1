import sys
import os

sys.path.append(os.path.abspath('./src'))
import utils
import logging
import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///shop.db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

app = FastAPI(
    title='Product Shop'
)


# Создание таблиц для покупателей и товаров
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


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Добавление продукта в БД
@app.post('/products/addproduct')
def add_product(name: str, price: int, restriction: bool) -> list:
    try:
        new_product = Product(name=name, price=price, restriction=restriction)
        session.add(new_product)
        session.commit()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]
    else:
        logger.info("Successfully registered product: %s",
                    {
                        'name': name,
                        'price': price,
                        'restriction': restriction
                    })
        return [{'code': 200,
                 'body': {
                     'name': name,
                     'price': price,
                     'restriction': restriction
                 }}]


# Изменение продукта в БД
@app.post('/products/changeproduct')
def change_product(id: int, name: str, price: int, restriction: bool) -> list:
    try:
        item_to_update = session.query(Product).filter_by(id=id).first()
        if item_to_update:
            item_to_update.name = name
            item_to_update.price = price
            item_to_update.restriction = restriction
            session.commit()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]
    else:
        logger.info("Successfully changed product: %s",
                    {
                        'id': id,
                        'name': name,
                        'price': price,
                        'restriction': restriction
                    })
        return [{'code': 200,
                 'body': {
                     'id': id,
                     'name': name,
                     'price': price,
                     'restriction': restriction
                 }}]


# Удаление продукта из БД
@app.post('/products/deleteproduct')
def delete_product(id: int) -> list:
    try:
        item_to_delete = session.query(Product).filter_by(id=id).first()
        if item_to_delete:
            session.delete(item_to_delete)
            session.commit()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]
    else:
        logger.info("Successfully deleted product: %s",
                    {
                        'id': id
                    })
        return [{'code': 200,
                 'body': {
                     'id': id
                 }}]


# Добавление покупателя в БД
@app.post('/customers/addcustomer')
def add_customer(name: str, age: int) -> list:
    try:
        new_customer = Customer(name=name, age=age)
        session.add(new_customer)
        session.commit()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]
    else:
        logger.info("Successfully registered product: %s",
                    {
                        'name': name,
                        'age': age,
                    })
        return [{'code': 200,
                 'body': {
                     'name': name,
                     'age': age,
                 }}]


# Изменение покупателя в БД
@app.post('/customers/changecustomer')
def change_customer(id: int, name: str, age: int) -> list:
    try:
        item_to_update = session.query(Customer).filter_by(id=id).first()
        if item_to_update:
            item_to_update.name = name
            item_to_update.age = age
            session.commit()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]
    else:
        logger.info("Successfully changed product: %s",
                    {
                        'id': id,
                        'name': name,
                        'age': age,
                    })
        return [{'code': 200,
                 'body': {
                     'id': id,
                     'name': name,
                     'age': age,
                 }}]


# Удаление продукта из БД
@app.post('/customers/deletecustomer')
def delete_customer(id: int) -> list:
    try:
        item_to_delete = session.query(Customer).filter_by(id=id).first()
        if item_to_delete:
            session.delete(item_to_delete)
            session.commit()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]
    else:
        logger.info("Successfully deleted customer: %s",
                    {
                        'id': id
                    })
        return [{'code': 200,
                 'body': {
                     'id': id
                 }}]


# Создание корзины
@app.post('/baskets/newbasket')
def new_basket(customer_id: int, product_ids: list) -> list:
    pass


if __name__ == "__main__":
    uvicorn.run("main:app")

session.close()
