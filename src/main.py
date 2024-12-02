import uvicorn
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from configs.env import IS_DEV_ENV
from controllers.user.auth_controller import auth_router
from controllers.user.user_controller import user_router
from ws import ws_manager

app = FastAPI(
    title="Dating API",
    description="API Dating",
    version="0.1.1",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth sector
app.include_router(auth_router)

# ############################### #

app.include_router(user_router)


# ############################### #


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    if IS_DEV_ENV:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8080,
            use_colors=True,
            reload=True,
            log_level="info",
        )
    else:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8080,
            use_colors=True,
            reload=False,
            log_level="info",
            ssl_keyfile="/app/key_file.pem",
            ssl_certfile="/app/ssl_cert.pem",
        )
