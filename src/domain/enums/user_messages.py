from enum import Enum


class UserMessage(str, Enum):
    NOT_FOUND = "user_not_found"
    NOT_CREATED = "user_not_created"
    USER_NOT_CREATED_SAVING_ERROR = "user_not_created_saving"
