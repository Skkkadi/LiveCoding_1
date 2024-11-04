from src.database import Base, engine, session

from src.routes.product import product_router
from src.routes.customer import customer_router
from src.routes.basket import basket_router
from src.routes.sell import sell_router

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title='Product Shop'
)

app.include_router(product_router, prefix="/api/v1")
app.include_router(customer_router, prefix="/api/v1")
app.include_router(basket_router, prefix="/api/v1")
app.include_router(sell_router, prefix="/api/v1")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    uvicorn.run("main:app")

session.close()
