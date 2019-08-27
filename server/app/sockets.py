from chat.sockets import personal


def init_ws(app):
    app.add_websocket_route(personal, "personal/")
