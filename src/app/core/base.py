from copy import deepcopy
from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def model_dump(self):
        dict_model = self.__dict__
        result: dict = deepcopy(dict_model)
        for key in dict_model.keys():
            if "__" in key or key.find("_") == 0:
                result.pop(key)
        return result
    
TModel = TypeVar("TModel", bound=Base)