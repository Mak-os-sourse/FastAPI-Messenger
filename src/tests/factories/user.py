from src.tests.factories.base import BaseFactory

from src.tests.fake import fake
from src.app.models.user import User

class UserFactory(BaseFactory):
    def __init__(self):
        super().__init__(User)
    
    def get_data(self):
        return {
            "username": fake.name(),
            "name": fake.name(),
            "password": fake.password(),
            "email": fake.email(),
            "description": fake.text(50),
            "secret_key": None,
            "type_2fa": "email",
        }

user_factory = UserFactory()