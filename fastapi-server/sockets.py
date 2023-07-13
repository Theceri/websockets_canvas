import socketio

sio_server = socketio.AsyncServer(
    async_mode = 'asgi',
    cors_allowed_origins = [] # Allow all origins
)

sio_app = socketio.ASGIApp(
    socketio_server = sio_server,
    socketio_path = 'sockets'
    # socketio_path='/sockets'# Use the same path as mounted in main.py
)

@sio_server.event
async def connect(sid, environ):
    print(f'Client connected: {sid}')

@sio_server.event
async def disconnect(sid):
    print(f'Client disconnected: {sid}')

@sio_server.event
async def client_ready(sid):
    print(f'{sid}: the client is ready')
    await sio_server.emit('get-canvas-state')

@sio_server.event
async def canvas_state(sid, state):
    print(f'{sid}: received canvas state')
    await sio_server.emit('canvas-state-from-server', state)

@sio_server.event
async def draw_line(sid, data):
    prev_point = data.get('prevPoint')
    current_point = data.get('currentPoint')
    color = data.get('color')  
    await sio_server.emit('draw-line', { 'prevPoint': prev_point, 'currentPoint': current_point, 'color': color })

@sio_server.event
async def clear(sid):    
    # await sio_server.emit('get-canvas-state', {'sid': sid})
    await sio_server.emit('clear')