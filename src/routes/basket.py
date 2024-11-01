from src.config import logger
from src.database import session
from src.models import Basket, Product, Customer
from fastapi import APIRouter

basket_router = APIRouter()


# Возвращает стоимость всех продуктов в корзине
# Если возраст покупателя не соответствует, продукт не учитывается и удаляется из нее
# Если покупатель не найден, возвращает -1
def calculate_price(product_ids: list, customer_id: int) -> int:
    total = 0
    try:
        this_customer = session.query(Customer).filter_by(id=customer_id).first()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return -1

    if this_customer.age >= 18:
        restricted = False
    else:
        restricted = True

    for id in product_ids:
        try:
            this_product = session.query(Product).filter_by(id=int(id)).first()
        except Exception as e:
            logger.error("Error with database: %s", e)
        else:
            if this_product.restriction and restricted:
                pass
            else:
                total += this_product.price
    return total


# Возвращает количество товаров, которые не прошли проверку на возраст
# Если покупатель не найден, возвращает -1
def check_restrictions(product_ids: list, customer_id: int) -> int:
    try:
        this_customer = session.query(Customer).filter_by(id=customer_id).first()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return -1

    restricted_products = 0
    if this_customer.age >= 18:
        restricted = False
    else:
        restricted = True

    for id in product_ids:
        try:
            this_product = session.query(Product).filter_by(id=int(id)).first()
        except Exception as e:
            logger.error("Error with database: %s", e)
        else:
            if this_product.restriction and restricted:
                restricted_products += 1
            else:
                pass
    return restricted_products


# Возвращает строку с товарами, прошедшими проверку
# Если покупатель не найден, возвращает -1
def get_unrestricted_products(product_ids: list, customer_id: int) -> int | str:
    try:
        this_customer = session.query(Customer).filter_by(id=customer_id).first()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return -1

    if this_customer.age >= 18:
        restricted = False
    else:
        restricted = True

    for id in product_ids:
        try:
            this_product = session.query(Product).filter_by(id=int(id)).first()
        except Exception as e:
            logger.error("Error with database: %s", e)
        else:
            if this_product.restriction and restricted:
                product_ids.remove(id)
            else:
                pass
    return product_ids


# Делает список из строки (для расчета стоимости, добавления, etc)
def get_product_list(product_string: str) -> list:
    try:
        product_list = []
        product_id = ''
        for i in product_string:
            if i != ' ':
                product_id += i
            else:
                product_list.append(int(product_id))
                product_id = ''
        else:
            product_list.append(int(product_id))
        return product_list
    except Exception as e:
        logger.error("Incorrect string: %s", e)
        return []


# Делает строку из списка (для хранения в БД)
def get_product_string(product_list: list) -> str:
    try:
        product_list = [str(i) for i in product_list]
        product_string = ' '.join(product_list)
        return product_string
    except Exception as e:
        logger.error("Incorrect list: %s", e)
        return ''


# Добавление продукта в корзину или ее создание, если корзины не существует
@basket_router.post('/baskets/addproduct')
def add_product(customer_id: int, product_id: int) -> list:
    item_to_update = session.query(Basket).filter_by(customer_id=customer_id).first()
    customer = session.query(Customer).filter_by(id=customer_id).first()
    product = session.query(Product).filter_by(id=product_id).first()
    if customer:
        if product:
            if item_to_update:
                products_list = get_product_list(item_to_update.product_ids)
                products_list.append(product_id)
                try:
                    item_to_update.product_ids = get_product_string(products_list)
                    session.commit()
                except Exception as e:
                    logger.error("Error with database: %s", e)
                    return [{'code': 500, 'body': 'InternalServerError: try again later'}]
                else:
                    logger.info("Successfully added product: %s",
                                {
                                    'customer_id': customer_id,
                                    'product_id': product_id,
                                    'product_list': products_list
                                })
                    return [{'code': 200,
                             'body': {
                                 'customer_id': customer_id,
                                 'product_id': product_id,
                                 'product_list': products_list
                             }}]
            else:
                try:
                    new_basket = Basket(customer_id=customer_id, product_ids=str(product_id))
                    session.add(new_basket)
                    session.commit()
                except Exception as e:
                    logger.error("Error with database: %s", e)
                    return [{'code': 500, 'body': 'InternalServerError: try again later'}]
                else:
                    logger.info("Successfully added product with basket creation: %s",
                                {
                                    'customer_id': customer_id,
                                    'product_id': product_id,
                                })
                    return [{'code': 200,
                             'body': {
                                 'customer_id': customer_id,
                                 'product_id': product_id,
                             }}]
        else:
            logger.info("Trying to add unexisting product to basket: %s", item_to_update.id)
            return [{'code': 404, 'body': 'Error: product not found'}]
    else:
        logger.info("Trying to add product for unregistered customer: %s", customer_id)
        return [{'code': 404, 'body': 'Error: customer not found'}]


# Удаление продукта из корзины
@basket_router.post('/baskets/removeproduct')
def remove_product(customer_id: int, product_id: int) -> list:
    item_to_update = session.query(Basket).filter_by(customer_id=customer_id).first()
    customer = session.query(Customer).filter_by(id=customer_id).first()
    product = session.query(Product).filter_by(id=product_id).first()
    if customer:
        if product:
            if item_to_update:
                products_list = get_product_list(item_to_update.product_ids)
                products_list.remove(product_id)
                try:
                    item_to_update.product_ids = get_product_string(products_list)
                    session.commit()
                except Exception as e:
                    logger.error("Error with database: %s", e)
                    return [{'code': 500, 'body': 'InternalServerError: try again later'}]
                else:
                    logger.info("Successfully removed product: %s",
                                {
                                    'customer_id': customer_id,
                                    'product_id': product_id,
                                    'product_list': products_list
                                })
                    return [{'code': 200,
                             'body': {
                                 'customer_id': customer_id,
                                 'product_id': product_id,
                                 'product_list': products_list
                             }}]
            else:
                logger.info("Trying to remove product from unexisting basket")
                return [{'code': 404, 'body': 'Error: basket not found'}]
        else:
            logger.info("Trying to add unexisting product to basket: %s", product_id)
            return [{'code': 404, 'body': 'Error: product not found'}]
    else:
        logger.info("Trying to add product for unregistered customer: %s", customer_id)
        return [{'code': 404, 'body': 'Error: customer not found'}]


# Получает информацию о корзине, удаляет запрещенные продукты, рассчитывает стоимость и записывает в бд
@basket_router.post('/baskets/getinfo')
def get_basket_info(id: int) -> list:
    try:
        item = session.query(Basket).filter_by(id=id).first()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return [{'code': 500, 'body': 'InternalServerError: try again later'}]
    else:
        if item:
            product_list = get_product_list(item.product_ids)
            restricted_products_count = check_restrictions(product_list, item.customer_id)
            unrestricted_products = get_unrestricted_products(product_list, item.customer_id)
            price = calculate_price(product_list, item.customer_id)
            item.total = price
            session.commit()
            logger.info('Successfully got info for basket: %s', id)
            return [{'code': 200,
                     'body': {
                         'basket_id': id,
                         'customer_id': item.customer_id,
                         'number_of_restricted_products': restricted_products_count,
                         'products_ids': unrestricted_products,
                         'price': price
                     }}]
        else:
            logger.info("Trying to remove product from unexisting basket: %s", id)
            return [{'code': 404, 'body': 'Error: basket not found'}]
