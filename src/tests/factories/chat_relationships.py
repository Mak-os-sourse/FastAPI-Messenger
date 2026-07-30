from factory import LazyAttribute, SubFactory

from app.models.chat_relationships import ChatRelationships
from tests.factories.base import BaseFactory
from tests.factories.chat_group import ChatGroupFactory
from tests.factories.user import UserFactory


class ChatRelationshipsFactory(BaseFactory):
    class Meta:
        model = ChatRelationships
        
    user = SubFactory(UserFactory)
    chat = SubFactory(ChatGroupFactory)

    user_id = LazyAttribute(lambda m: m.user.id)
    chat_id = LazyAttribute(lambda m: m.chat.id)
    is_admin: bool