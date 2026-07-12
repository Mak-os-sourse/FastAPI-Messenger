import time
from typing import Literal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.app.core.base import Base

class Chat(Base):
    __tablename__ = "Chats"
    
    id: Mapped[int] = mapped_column(ForeignKey("ChatRelationships.chat_id"), primary_key=True, autoincrement=True)
    type: Mapped[Literal["direct", "group"]]
    name: Mapped[str] = mapped_column(nullable=True)
    create_at: Mapped[int] = mapped_column(default=lambda: int(time.time()))
    
    chat_relationships: Mapped["ChatRelationships"] = relationship(uselist=True, lazy="selectin")