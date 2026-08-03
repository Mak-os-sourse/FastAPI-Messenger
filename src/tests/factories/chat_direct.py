
from app.models.chat_direct import ChatDirect
from tests.factories.base import BaseFactory


class ChatDirectFactory(BaseFactory):
    class Meta:
        model = ChatDirect
        
    user_id_one: int
    user_id_two: int