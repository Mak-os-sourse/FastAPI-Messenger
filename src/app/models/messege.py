from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.app.core.base import Base

class Messege(Base):
    __tablename__ = "Messeges"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    content: Mapped[str] = mapped_column()
    
    user: Mapped["User"] = relationship(lazy="selectin")