import time
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.base import Base

class ChatDirect(Base):
    __tablename__ = "ChatsDirect"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id_one: Mapped[int] = mapped_column()
    user_id_two: Mapped[int] = mapped_column()
    create_at: Mapped[int] = mapped_column(default=lambda: int(time.time()))