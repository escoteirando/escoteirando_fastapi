__all__ = ['app', 'Config', 'get_logger']

from fastapi import FastAPI

from src import __appname__, __description__, __version__
from src.app.config import Config
from src.app.logger import get_logger
from src.app.setup_services import setup

get_logger(__name__).info('INIT APP - %s:%s',
                          __appname__,
                          __version__)

app = FastAPI(title=__appname__,
              description=__description__,
              version=__version__)


setup(app)
