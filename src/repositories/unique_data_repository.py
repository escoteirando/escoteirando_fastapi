from pymongo.collection import Collection

from src.app import get_logger
from src.cross_cutting import Singleton

logger = get_logger(__name__)


@Singleton
class UniqueDataRepository:
    def __init__(self, connection):
        self._collection: Collection = connection.collection("_unique")
        logger.info("INIT")

    def set(self, key, value):
        try:
            result = self._collection.replace_one({"_id": key}, value, upsert=True)
            return result.upserted_id or result.modified_count

        except Exception as exc:
            logger.exception(
                "Error on setting unique data {0}: {1} - {2}", key, value, exc
            )

    def get(self, key):
        try:
            result = self._collection.find_one({"_id": key})
            return result
        except Exception as exc:
            logger.exception("Error on getting unique data {0} - {1}", key, exc)

    def set_values(self, values: list):
        try:

            bulk = self._collection.initialize_ordered_bulk_op()

            for value in values:
                if "_id" in value:
                    bulk.find({"_id": value["_id"]}).remove()
                    bulk.insert(value)

            result = bulk.execute()
            return result
        except Exception as exc:
            logger.exception(
                "Error on setting list of unique data {0} - {1}", values, exc
            )
