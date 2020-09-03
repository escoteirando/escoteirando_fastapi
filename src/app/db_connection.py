import datetime
from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection, IndexModel
from pymongo.database import Database

from src.app import get_logger
from src.exceptions import DBConnectionException
from src.repositories.unique_data_repository import UniqueDataRepository

logger = get_logger(__name__)


class DBConnection:
    def __init__(self, config):
        if not config.MONGODB_URI:
            raise DBConnectionException("Missing MONGODB_URI environment variable")

        self._client = MongoClient(config.MONGODB_URI)
        try:
            info = self._client.server_info()
            logger.debug(info)
            self._database_name = config.MONGODB_DATABASE
            self._database: Database = self._client.get_database(self._database_name)
        except Exception as exc:
            raise DBConnectionException("Error on connecting to MongoDB", str(exc))
        if not self._database_name:
            raise DBConnectionException("Missing MONGODB_DATABASE environment variable")

        self._collections = {}

        self.update_running()

        logger.info("INIT")

    def update_running(self):
        unique_repo = UniqueDataRepository.Instance(self)
        running_data = unique_repo.get("running") or {
            "install": datetime.datetime.utcnow(),
            "last_run": datetime.datetime.utcnow(),
            "start_count": 0,
        }
        running_data["last_run"] = datetime.datetime.utcnow()
        running_data["start_count"] += 1
        unique_repo.set("running", running_data)

    @property
    def client(self) -> MongoClient:
        return self._client

    @property
    def database(self) -> Database:
        return self._database

    def collection(
        self, collection_name, index_defs: List[IndexModel] = None
    ) -> Collection:
        if collection_name not in self._collections:
            col = Collection(self._database, collection_name)
            if isinstance(index_defs, list):
                col.create_indexes(index_defs)

            self._collections[collection_name] = col

        return self._collections[collection_name]
