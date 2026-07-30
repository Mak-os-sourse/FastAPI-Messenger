import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base import Base


class Messege(Base):
    __tablename__ = "Messeges"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    content: Mapped[str] = mapped_column()
    create_at: Mapped[int] = mapped_column(default=lambda: int(time.time()))
    
    user: Mapped["User"] = relationship(lazy="selectin")