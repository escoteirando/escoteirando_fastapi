import logging
import logging.config
import os

from fastapi import FastAPI

from src.app.config import Config
from src.app.db_connection import DBConnection
from src.app.static_files import setup_static_files

from src.repositories import UserRepository
from src.services.authorization_service import AuthorizationService
from src.services.cache_memory_service import CacheMemoryService
from src.services.user_service import UserService
from src.services.mailer_service import MailerService

logging.config.fileConfig(
    os.path.join('src', 'logging.conf'),
    disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def setup(app: FastAPI):
    logger.info('INIT')
    config = Config()
    setattr(app, 'CONFIG', config)
    db_connection = DBConnection(config)
    setattr(app, 'DBCONNECTION', db_connection)

    setup_static_files(app)
    cache_service = CacheMemoryService()
    setattr(app, 'CACHE', cache_service)

    mailer_service = MailerService.Instance(config)
    setattr(app, 'MAILER', mailer_service)

    user_repository = UserRepository(db_connection)

    user_service = UserService(user_repository, mailer_service)
    setattr(app, 'USER', user_service)
    authorization_service = AuthorizationService(
        cache_service, user_service, config)
    setattr(app, 'AUTH', authorization_service)

    logger.info('END')
