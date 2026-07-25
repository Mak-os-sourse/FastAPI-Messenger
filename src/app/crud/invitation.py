from app.crud.base import BaseCRUD
from app.models.invitation import Invitation

invitation_crud = BaseCRUD(Invitation)