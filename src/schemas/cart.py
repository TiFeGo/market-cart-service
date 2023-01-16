import pydantic
import uuid


class BaseCart(pydantic.BaseModel):
    user_id: int
    products_uuid: list[uuid.UUID]
    amount: int


class Cart(BaseCart):
    cart_uuid: uuid.UUID


class CreateItem(pydantic.BaseModel):
    user_id: int
    product_uuid: uuid.UUID
    amount: int