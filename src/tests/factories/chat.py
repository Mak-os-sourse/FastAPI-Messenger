from src.tests.factories.base import BaseFactory

from src.tests.fake import fake
from src.app.models.chat import Chat

class ChatFactory(BaseFactory):
    class Meta:
        model = Chat
        
    type: str = "group"
    name: str = fake.name()
    description: str = fake.text(50)
    