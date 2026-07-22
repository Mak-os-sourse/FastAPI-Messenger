import time
from typing import Literal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.app.core.base import Base

class ChatGroup(Base):
    __tablename__ = "ChatGroups"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[Literal["public", "private"]]
    name: Mapped[str] = mapped_column(String(length=30), nullable=True)
    description: Mapped[str] = mapped_column(String(length=50), nullable=True)
    admin_only: Mapped[bool] = mapped_column()
    create_at: Mapped[int] = mapped_column(default=lambda: int(time.time()))
    