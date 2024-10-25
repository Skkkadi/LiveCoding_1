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


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Basket:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.product_ids = []

    def add_product(self, product_id):
        """Добавляет товар в корзину."""
        if product_id not in self.product_ids:
            self.product_ids.append(product_id)

    def remove_product(self, product_id):
        """Удаляет товар из корзины."""
        if product_id in self.product_ids:
            self.product_ids.remove(product_id)


baskets = []


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


# Создание корзины (не доделано и не проверялось)
@app.post('/addbasket')
def add_basket(customer_id: int, product_ids: list) -> list:
    try:
        basket = Basket(customer_id)
        for product_id in product_ids:
            basket.add_product(product_id)
            baskets.append(basket)
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]


if __name__ == "__main__":
    uvicorn.run("main:app")

session.close()
