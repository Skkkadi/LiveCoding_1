from src.config import logger
from src.database import session
from src.models import Customer
from fastapi import APIRouter

customer_router = APIRouter()


# Добавление покупателя в БД
@customer_router.post('/customers/addcustomer')
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
@customer_router.post('/customers/changecustomer')
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
@customer_router.post('/customers/deletecustomer')
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
