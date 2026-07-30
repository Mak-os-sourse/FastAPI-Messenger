import uvicorn
from fastapi import FastAPI

from app.api.v1 import router as ws_router
from app.core.lifespan import lifespan
from app.websocket import router

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(ws_router)

@app.get("/ping")
async def pong():
    return "pong"

if __name__ == "__main__":
    uvicorn.run(app)
