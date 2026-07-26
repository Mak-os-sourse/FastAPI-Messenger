from httpx import AsyncClient
from httpx_ws import aconnect_ws

from tests.factories.chat_relationships import ChatRelationshipsFactory
from app.schemas.messege import NewMessegeRequest
from tests.fake import fake

async def test_new_messege(ws_client: AsyncClient, auth_user):
    chat = await ChatRelationshipsFactory.create()
    auth_user(chat.user)
    
    async with aconnect_ws("http://testserver/ws", ws_client) as ws:
        n = NewMessegeRequest(action="NewMessege", chat_id=chat.chat_id, content=fake.text()).model_dump()
        await ws.send_json(n)
        data = await ws.receive_json()  