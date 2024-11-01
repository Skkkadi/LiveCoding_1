# Возвращает стоимость всех продуктов в корзине
# Если возраст покупателя не соответствует, продукт не учитывается и удаляется из нее
# Если покупатель не найден, возвращает -1
def calculate_price(product_ids: string, customer_id: int) -> int:
    total = 0
    try:
        this_customer = session.query(Product).filter_by(id=customer_id).first()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return -1

    restricted = False if this_customer.age >= 18 else restricted = True
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
def check_restrictions(product_ids: string, customer_id: int) -> int:
    try:
        this_customer = session.query(Product).filter_by(id=customer_id).first()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return -1

    restricted_products = 0
    restricted = False if this_customer.age >= 18 else restricted = True
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
def get_unrestricted_products(product_ids: string, customer_id: int) -> int:
    try:
        this_customer = session.query(Product).filter_by(id=customer_id).first()
    except Exception as e:
        logger.error("Error with database: %s", e)
        return -1

    restricted = False if this_customer.age >= 18 else restricted = True
    for id in product_ids:
        try:
            this_product = session.query(Product).filter_by(id=int(id)).first()
        except Exception as e:
            logger.error("Error with database: %s", e)
        else:
            if this_product.restriction and restricted:
                product_ids = product_ids.replace(id, '')
            else:
                pass
    return product_ids
