from datetime import date, datetime

from pydantic import BaseModel
from pymongo.collection import Collection, InsertOneResult, UpdateResult

from src.app import get_logger
from src.exceptions import RepositoryException

from .autoinc_repository import AutoIncRepository

logger = get_logger(__name__)

_auto_inc_repository = None


class BaseRepository:
    def __init__(self, connection, entity_type, collection_name=None):
        global _auto_inc_repository
        _auto_inc_repository = AutoIncRepository.Instance(connection)

        class_name = str(self.__class__).split("'")[1].split(".")[-1]

        self.logger = get_logger(class_name)
        if not issubclass(entity_type, BaseModel):
            raise RepositoryException(
                "Entity type is not a BaseModel", entity_type)

        entity_name = str(entity_type).split("'")[1].split(".")[-1]
        self._entity_type = entity_type

        self._collection_name = collection_name or entity_name

        self._collection: Collection = connection.collection(
            self._collection_name)
        self._connection = connection
        self.logger.info(
            "INIT COLLECTION %s FOR ENTITY %s",
            self._collection_name, entity_name
        )

    @property
    def collection(self) -> Collection:
        return self._collection

    def save(self, model: BaseModel):
        if not isinstance(model, self._entity_type):
            raise RepositoryException(
                "Model {0} ({1}) is not a ({2}})",
                repr(model),
                model.__class__,
                self._entity_type,
            )

        try:
            if model.id <= 0:
                # Insert
                as_dict = self.check_types(model.dict())
                as_dict["_id"] = _auto_inc_repository.get_next_id(
                    self._collection_name)

                result: InsertOneResult = self._collection.insert_one(as_dict)
                if result.inserted_id:
                    as_dict["id"] = as_dict["_id"]
                    return self._entity_type(**as_dict)
            else:
                as_dict = self.check_types(model.dict())
                as_dict["_id"] = as_dict["id"]
                del as_dict["id"]
                result: UpdateResult = self._collection.replace_one(
                    filter={"_id": model.id}, replacement=as_dict, upsert=True
                )
                if result.upserted_id:
                    setattr(model, "_id", result.upserted_id)
                    return True
                elif result.modified_count > 0:
                    return True

        except Exception as exc:
            self.logger.error("ERROR ON SAVING MODEL %s: %s", model, exc)

    def check_types(self, model: dict):
        """Garantir que não existam dados inválidos para gravar no MongoDB"""
        for key in model.keys():
            if model.get(key).__class__ == date:
                model[key] = datetime(
                    model[key].year, model[key].month, model[key].day)
        return model
