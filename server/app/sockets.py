from chat.sockets import chat


def init_ws(app):
    app.add_websocket_route(chat, "chat/<pk>")
    
# https://github.com/suhjohn/Sanic-Chat-Example/blob/master/backend/websockets.py