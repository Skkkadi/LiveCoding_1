from src.config import logger
from src.database import session
from src.models import Product
from fastapi import APIRouter

product_router = APIRouter()

# Добавление продукта в БД
@product_router.post('/products/addproduct')
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
@product_router.post('/products/changeproduct')
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
@product_router.post('/products/deleteproduct/{id}')
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
