from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.app import get_logger

logger = get_logger(__name__)


def setup_static_files(app: FastAPI):
    logger.info("INIT")
    app.mount(
        '/f',
        StaticFiles(directory="static", html=True),
        name="static")
