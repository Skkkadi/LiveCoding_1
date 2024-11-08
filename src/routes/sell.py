from src.config import logger
from src.database import session
from src.models import Basket, Sell
from fastapi import APIRouter

sell_router = APIRouter()


# Завершает сделку, очищает корзину пользователя, записывает сделку в БД
@sell_router.post('/sells/finishsell/{basket_id}')
def finish_sell(basket_id: int) -> list:
    item = session.query(Basket).filter_by(id=basket_id).first()
    if item:
        if item.total:
            if item.product_ids != '':
                new_sell = Sell(customer_id=item.customer_id, basket_id=item.id, total=item.total)
                session.add(new_sell)
                item.total = 0
                item.product_ids = ''
                session.commit()
                logger.info(f'Sell for basket {item.id} finished')
                return [{
                    'code': 200,
                    'body': f'Sell for basket {item.id} finished'
                }]
            else:
                return [{
                    'code': 412,
                    'body': 'Basket is empty'
                }]
        else:
            return [{
                'code': 412,
                'body': 'Basket was not confirmed'
            }]
    else:
        return [{
            'code': 404,
            'body': 'Basket not found'
        }]

