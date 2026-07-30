from factory import LazyAttribute, SubFactory

from app.models.invitation import Invitation
from tests.factories.base import BaseFactory
from tests.factories.user import UserFactory


class InvitationFactory(BaseFactory):
    class Meta:
        model = Invitation
        
    user = SubFactory(UserFactory)

    user_id = LazyAttribute(lambda m: m.user.id)
    chat_id = LazyAttribute(lambda m: m.chat.id)