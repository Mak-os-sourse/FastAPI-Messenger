from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.app.core.base import Base

class Invitation(Base):
    __tablename__ = "Invitation"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    
    user: Mapped["User"] = relationship(lazy="selectin")