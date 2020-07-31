__all__ = ['app', 'Config']

from fastapi import FastAPI
from src import __version__, __description__, __appname__
from src.app.setup_services import setup
from src.app.config import Config

app = FastAPI(title=__appname__,
              description=__description__,
              version=__version__)


setup(app)
