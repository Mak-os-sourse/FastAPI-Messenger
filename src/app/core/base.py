from copy import deepcopy
from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def model_dump(self) -> Any:
        dict_model = self.__dict__
        result: dict[Any, Any] = deepcopy(dict_model)
        for key in dict_model:
            if "__" in key or key.find("_") == 0:
                result.pop(key)
        return result
