from fastapi import APIRouter, Depends, status, HTTPException

from src.core import tracing_tools
from src.schemas import cart as schemas
from src.models import cart as models
from src.utils import mappers
from src.endpoints import services

cart_router = APIRouter(
    tags=['Cart'],
    prefix='/cart'
)


@cart_router.get('/{user_id}', response_model=schemas.Cart, status_code=status.HTTP_200_OK)
@tracing_tools.trace_it('Endpoint', 'Get cart by user id')
async def get_cart_by_user_id(user_id: int) -> schemas.Cart:
    cart = await services.get_cart_by_user_id(user_id)
    return mappers.mapping_model_schema(cart)


@cart_router.post('/add', response_model=schemas.Cart, status_code=status.HTTP_201_CREATED)
@tracing_tools.trace_it('Endpoint', 'Add item')
async def add_item(item: schemas.CreateItem) -> schemas.Cart:
    cart = await services.add_item(item)
    return mappers.mapping_model_schema(cart)


@cart_router.post('/confirm', response_model=dict, status_code=status.HTTP_200_OK)
@tracing_tools.trace_it('Endpoint', 'Confirm')
async def confirm(user_id) -> dict:
    return await services.confirm(user_id)
