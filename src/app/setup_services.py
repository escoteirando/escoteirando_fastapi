from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cache_gs import CacheGS
from src.app import get_logger
from src.app.config import Config
from src.app.db_connection import DBConnection
from src.app.static_files import setup_static_files
from src.repositories import AtividadeRepository, UserRepository, MAPPAKBProgressaoRepository
from src.services.atividade_service import AtividadeService
from src.services.authorization_service import AuthorizationService
# from src.services.cache_memory_service import CacheMemoryService
from src.services.mailer_service import MailerService
from src.services.mappa_service import MAPPA_Service
from src.services.user.user_password_service import UserPasswordService
from src.services.user_service import UserService

logger = get_logger(__name__)


def setup(app: FastAPI):
    logger.info("INIT")
    config = Config()
    setattr(app, "CONFIG", config)
    db_connection = DBConnection(config)
    setattr(app, "DBCONNECTION", db_connection)

    setup_static_files(app)

    cache_service = CacheGS(config.CACHE_CONFIG)
    # cache_service = CacheMemoryService()
    setattr(app, "CACHE", cache_service)

    mailer_service = MailerService.Instance(config)
    setattr(app, "MAILER", mailer_service)

    user_repository = UserRepository(db_connection)

    user_service = UserService(user_repository)
    setattr(app, "USERS", user_service)

    mappa_kb_progressao_repository = MAPPAKBProgressaoRepository(db_connection)
    mappa_service = MAPPA_Service(
        cache_service, user_service, mappa_kb_progressao_repository)
    setattr(app, "MAPPA", mappa_service)

    user_password_service = UserPasswordService(
        cache_service, user_service, mailer_service
    )
    setattr(app, "USER_PASS", user_password_service)

    authorization_service = AuthorizationService(
        cache_service, user_service, config)
    setattr(app, "AUTH", authorization_service)

    atividade_repository = AtividadeRepository(db_connection)
    atividade_service = AtividadeService(atividade_repository)
    setattr(app, "ATV", atividade_service)

    app.add_middleware(
        CORSMiddleware,
        # allow_origins=['*'],
        allow_origin_regex="http?://.*",
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("END")
    return app
