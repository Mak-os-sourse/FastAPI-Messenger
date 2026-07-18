from src.tests.factories.base import BaseFactory

from factory.faker import Faker
from src.app.models.chat_group import ChatGroup

class ChatGroupFactory(BaseFactory):
    class Meta:
        model = ChatGroup
        
    type: str = "public"
    name: str = Faker("name")
    description = Faker("text", max_nb_chars=50)
    admin_only: bool = False