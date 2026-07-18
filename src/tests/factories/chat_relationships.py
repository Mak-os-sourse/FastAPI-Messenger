from src.tests.factories.base import BaseFactory

from factory import SubFactory, LazyAttribute
from src.tests.factories.user import UserFactory
from src.tests.factories.chat_group import ChatGroupFactory
from src.app.models.chat_relationships import ChatRelationships

class ChatRelationshipsFactory(BaseFactory):
    class Meta:
        model = ChatRelationships
        
    user = SubFactory(UserFactory)
    chat = SubFactory(ChatGroupFactory)

    user_id = LazyAttribute(lambda o: o.user.id)
    chat_id = LazyAttribute(lambda o: o.chat.id)
    is_admin: bool