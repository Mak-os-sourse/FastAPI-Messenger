from factory.faker import Faker

from app.models.user import User
from tests.factories.base import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = User
        
    username = Faker("name")
    name = Faker("name")
    password = Faker("password")
    email = Faker("email")
    description = Faker("text", max_nb_chars=50)
    secret_key = None
    type_2fa = "email"
    type_status = None