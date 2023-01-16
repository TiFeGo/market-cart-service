import uuid

from src.schemas import cart as schema
from src.models import cart as model
from src.broker import producer
from src.core import tracing_tools


@tracing_tools.trace_it('Service', 'get_cart_by_user_id')
async def get_cart_by_user_id(user_id: int) -> model.CartItem:
    return model.CartItem.objects(user_id=user_id).first()


@tracing_tools.trace_it('Service', 'add_item')
async def add_item(item: schema.CreateItem) -> model.CartItem:
    cart = model.CartItem.objects(user_id=item.user_id).first()
    if cart is None:
        cart = model.CartItem(
            cart_uuid=uuid.uuid4(),
            user_id=item.user_id,
            products_uuid=[item.product_uuid],
            amount=item.amount,
        )
        cart = cart.save()
    else:
        cart.products_uuid.append(item.product_uuid)
        cart.amount += item.amount
        cart = cart.save()
    return cart


@tracing_tools.trace_it('Service', 'Confirm')
async def confirm(user_id: int) -> dict:
    cart = model.CartItem.objects(user_id=user_id).first()
    delivery_info = producer.AddDelivery(
        method=producer.Method.CREATE,
        user_id=user_id,
        cart_uuid=str(cart.cart_uuid)
    )
    await producer.send_rabbitmq(delivery_info)
    return {'Result': 'Ok'}
