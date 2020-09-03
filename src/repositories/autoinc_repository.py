import datetime

from pymongo.database import Database

from src.app import get_logger
from src.cross_cutting import Singleton

from .unique_data_repository import UniqueDataRepository

logger = get_logger(__name__)


@Singleton
class AutoIncRepository:
    LAST_CHECK_ID = "_ai_last_check"
    LAST_CHECK = "last_check"
    LAST_ID = "last_id"

    def __init__(self, connection):
        self._connection = connection
        self._repo = UniqueDataRepository.Instance(connection)
        self.check_counters()

        logger.info("INIT")

    def check_counters(self):
        last_check = self._repo.get(self.LAST_CHECK_ID) or {
            self.LAST_CHECK: datetime.datetime.now()
        }
        time_pass = datetime.datetime.now() - last_check[self.LAST_CHECK]
        if time_pass.days < 1:
            return
        self.refresh_counters()
        self._repo.set(self.LAST_CHECK_ID, {self.LAST_CHECK: datetime.datetime.now()})

    def refresh_counters(self):
        database: Database = self._connection.database
        max_ids = []
        for collection_name in database.list_collection_names():
            if collection_name.startswith("_"):
                continue
            collection = database.get_collection(collection_name)
            max_id = collection.find_one(sort=[("_id", -1)])["_id"]
            max_ids.append({"_id": "_ai_" + collection_name, self.LAST_ID: max_id})
        logger.info("Updating auto_increment counters")
        self._repo.set_values(max_ids)

    def get_next_id(self, collection_name) -> int:
        data = {
            "_id": "_ai_" + collection_name,
            self.LAST_ID: self.get_current_id(collection_name),
        }
        data[self.LAST_ID] += 1
        if self._repo.set("_ai_" + collection_name, data):
            return data[self.LAST_ID]
        return 0

    def get_current_id(self, collection_name) -> int:
        data = self._repo.get("_ai_" + collection_name)
        if not data:
            return 0
        return data[self.LAST_ID]
