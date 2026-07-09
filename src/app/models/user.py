import time
from typing import Literal
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.base import Base

class User(Base):
    __tablename__ = "Users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(String(length=50))
    secret_key: Mapped[str] = mapped_column(nullable=True)
    type_2fa: Mapped[str] = mapped_column(nullable=True)
    create_at: Mapped[int] = mapped_column(default=lambda: int(time.time()))