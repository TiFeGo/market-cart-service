import pydantic
import uuid
import enum
import json
import aio_pika
from src.core.settings import settings


class Method(str, enum.Enum):
    CREATE = 'create'


class AddDelivery(pydantic.BaseModel):
    method: Method
    user_id: int
    cart_uuid: str


async def send_rabbitmq(msg: AddDelivery):
    connection = await aio_pika.connect(settings.RABBIT_URL)

    channel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(json.dumps(msg.dict()).encode("utf-8")),
        routing_key="fastapi_task"
    )

    await connection.close()
