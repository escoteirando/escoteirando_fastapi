__all__ = ["app", "Config", "get_logger"]

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src import __appname__, __description__, __version__
from src.app.config import Config
from src.app.logger import get_logger
from src.app.setup_services import setup

get_logger(__name__).info("INIT APP - %s:%s", __appname__, __version__)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=__appname__,
        version=__version__,
        description=__description__,
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = setup(
    FastAPI(
        title=__appname__,
        description=__description__,
        version=__version__))

app.openapi = custom_openapi
