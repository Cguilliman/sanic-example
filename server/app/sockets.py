from chat.sockets import chat


def init_ws(app):
    app.add_websocket_route(chat, "chat/<pk>")
