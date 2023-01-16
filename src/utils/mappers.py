import src.schemas.cart as schemas
import src.models.cart as models
from src.core import tracing_tools

from jaeger_client import Tracer
from opentracing_instrumentation.request_context import get_current_span, span_in_context


@tracing_tools.trace_it_sync(tag='mapper', value='model to schema')
def mapping_model_schema(model: models.CartItem):
    schema = schemas.Cart(
        cart_uuid=model.cart_uuid,
        user_id=model.user_id,
        products_uuid=model.products_uuid,
        amount=model.amount,
    )
    return schema


@tracing_tools.trace_it_sync(tag='mapper', value='schema to model')
def mapping_schema_model(schema: schemas.Cart):
    model = models.CartItem(
        cart_uuid=schema.cart_uuid,
        user_id=schema.user_id,
        products_uuid=schema.products_uuid,
        amount=schema.amount,
    )
    return model

