from src.tests.factories.base import BaseFactory

from src.tests.fake import fake
from src.app.models.user import User

class UserFactory(BaseFactory):
    class Meta:
        model = User
        
    username = fake.name()
    name = fake.name()
    password = fake.password()
    email = fake.email()
    description = fake.text(50)
    secret_key = None
    type_2fa = "email"
    type_status = None
    