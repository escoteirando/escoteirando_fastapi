import logging
import datetime
from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection, IndexModel
from pymongo.database import Database

from src.exceptions import DBConnectionException

logger = logging.getLogger(__name__)


class DBConnection:

    def __init__(self, config):
        if not config.MONGODB_URI:
            raise DBConnectionException(
                "Missing MONGODB_URI environment variable")

        self._client = MongoClient(config.MONGODB_URI)
        try:
            info = self._client.server_info()
            logger.debug(info)
            self._database_name = config.MONGODB_DATABASE
            self._database: Database = self._client.get_database(
                self._database_name)
        except Exception as exc:
            raise DBConnectionException(
                "Error on connecting to MongoDB", str(exc))
        if not self._database_name:
            raise DBConnectionException(
                "Missing MONGODB_DATABASE environment variable")

        self._collections = {}

        self.update_running()

        logger.info("INIT")

    def update_running(self):
        running_collection = self.collection('running')
        basic_running = {
            "_id": "unique",
            "install": datetime.datetime.utcnow(),
            "last_run": datetime.datetime.utcnow(),
            "start_count": 1
        }
        running_data = running_collection.find_one({"_id": "unique"})
        if running_data:
            basic_running.update(running_data)
            basic_running["start_count"] += 1
            basic_running["last_run"] = datetime.datetime.utcnow()

        try:
            saved = running_collection.replace_one(
                filter={"_id": "unique"},
                replacement=basic_running,
                upsert=True)
            logging.debug(saved)
        except Exception as exc:
            logging.error(str(exc))

    @property
    def client(self) -> MongoClient:
        return self._client

    def collection(self, collection_name,
                   index_defs: List[IndexModel] = None) -> Collection:
        if collection_name not in self._collections:
            col = Collection(self._database, collection_name)
            if isinstance(index_defs, list):
                col.create_indexes(index_defs)

            self._collections[collection_name] = col

        return self._collections[collection_name]
