import time
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.base import Base

class ChatDirect(Base):
    __tablename__ = "ChatDirects"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id_one: Mapped[int] = mapped_column()
    user_id_two: Mapped[int] = mapped_column()
    create_at: Mapped[int] = mapped_column(default=lambda: int(time.time()))
    
    __table_args__ = (UniqueConstraint("user_id_one", "user_id_two", name="unique_user_ids"), )