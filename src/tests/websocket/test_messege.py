from httpx_ws import AsyncWebSocketSession

from app.schemas.messege import NewMessegeRequest
from tests.factories.chat_relationships import ChatRelationshipsFactory
from tests.fake import fake


async def test_new_messege(ws_client, auth_user):
    chat = await ChatRelationshipsFactory.create()
    auth_user(chat.user)
    
    async with ws_client(chat.user_id) as ws:
        ws: AsyncWebSocketSession
        model = NewMessegeRequest(action="NewMessege", chat_id=chat.chat_id, content=fake.text(50), token="").model_dump()
        await ws.send_json(model)
        data = await ws.receive_json()
        
        assert data["status"] == "success"
        assert data["data"]["chat_id"] == chat.chat_id