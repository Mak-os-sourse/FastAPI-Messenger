from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.app.core.base import Base

class ChatRelationships(Base):
    __tablename__ = "ChatRelationships"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    is_admin: Mapped[bool] = mapped_column(default=False)
    
    user: Mapped["User"] = relationship(lazy="joined")
    chat: Mapped["ChatGroup"] = relationship(lazy="joined")