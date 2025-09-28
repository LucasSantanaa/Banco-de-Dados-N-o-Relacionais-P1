"""Inicializa FastAPI e WebSockets."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .routes import messages as messages_router
from .ws_manager import WSManager
from .database import get_db
from .models import serialize

app = FastAPI(title='FastAPI Chat Refatorado')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

manager = WSManager()
app.mount('/static', StaticFiles(directory='app/static'), name='static')

@app.get('/', include_in_schema=False)
async def index():
    return FileResponse('app/static/index.html')

app.include_router(messages_router.router)

@app.websocket('/ws/{room}')
async def ws_room(ws: WebSocket, room: str):
    await manager.connect(room, ws)
    try:
        cursor = get_db()['messages'].find({'room': room}).sort('_id', -1).limit(20)
        items = [serialize(d) async for d in cursor]
        items.reverse()
        await ws.send_json({'type': 'history', 'items': items})

        while True:
            payload = await ws.receive_json()
            username = str(payload.get('username', 'anon'))[:50]
            content = str(payload.get('content', '')).strip()
            if not content:
                continue
            doc = {
                'room': room,
                'username': username,
                'content': content,
                'created_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc),
            }
            res = await get_db()['messages'].insert_one(doc)
            doc['_id'] = res.inserted_id
            await manager.broadcast(room, {'type': 'message', 'item': serialize(doc)})
    except WebSocketDisconnect:
        manager.disconnect(room, ws)
