from factory.faker import Faker

from app.models.chat_group import ChatGroup
from tests.factories.base import BaseFactory


class ChatGroupFactory(BaseFactory):
    class Meta:
        model = ChatGroup
        
    type: str = "public"
    name: str = Faker("name")
    description = Faker("text", max_nb_chars=50)
    admin_only: bool = False