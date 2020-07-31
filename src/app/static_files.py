from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging


def setup_static_files(app: FastAPI):
    logging.getLogger(__name__).info("INIT")
    app.mount(
        '/f',
        StaticFiles(directory="static", html=True),
        name="static")
