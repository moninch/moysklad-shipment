from pydantic import BaseModel


class Position(BaseModel):
    quantity: float
    price: float
    product_id: str
