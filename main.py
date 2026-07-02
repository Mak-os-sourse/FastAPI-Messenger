import uvicorn
from fastapi import FastAPI

from src.app.core.lifespan import lifespan
from src.app.api.v1 import router

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/ping")
async def pong():
    return "pong"

if __name__ == "__main__":
    uvicorn.run(app)
