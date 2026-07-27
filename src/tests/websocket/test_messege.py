from starlette.testclient import WebSocketTestSession

from tests.factories.chat_relationships import ChatRelationshipsFactory
from app.schemas.messege import NewMessegeRequest
from tests.fake import fake

async def test_new_messege(ws_client: WebSocketTestSession, auth_user):
    chat = await ChatRelationshipsFactory.create()
    auth_user(chat.user)
    
    n = NewMessegeRequest(action="NewMessege", chat_id=chat.chat_id, content=fake.text(50), token="").model_dump()
    await ws_client.send_json(n)
    data = await ws_client.receive_json()
    print(data)
    ws_client.close()