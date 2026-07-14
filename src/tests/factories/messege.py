import factory
from src.tests.factories.base import BaseFactory

from src.tests.fake import fake
from src.app.models.messege import Messege

class ChatFactory(BaseFactory):
    class Meta:
        model = Messege
        
    chat_id: int = None
    