from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mongoengine import connect, disconnect

from prometheus_fastapi_instrumentator import Instrumentator

from src.core import tracing_tools
from src.core.settings import settings
from src.endpoints.router import cart_router

app = FastAPI(
    title='Ecommerce API',
    version='0.0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
    tracing_tools.init_tracer()
    connect(
        host=f'mongodb://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?authSource={settings.DATABASE_USERNAME}')


@app.on_event("shutdown")
def shutdown_event():
    disconnect()


app.include_router(cart_router)
