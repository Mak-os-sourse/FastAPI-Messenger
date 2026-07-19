from src.tests.factories.base import BaseFactory

from factory import SubFactory, LazyAttribute
from src.tests.factories.user import UserFactory
from src.tests.factories.chat_group import ChatGroupFactory
from src.app.models.invitation import Invitation

class InvitationFactory(BaseFactory):
    class Meta:
        model = Invitation
        
    user = SubFactory(UserFactory)

    user_id = LazyAttribute(lambda m: m.user.id)
    chat_id = LazyAttribute(lambda m: m.chat.id)