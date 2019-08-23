from users.routers import main, login, register, receive
from chat.routers import room_messages, create_room


def init_routers(app):
    app.add_route(main, "/", methods=["GET"])
    app.add_route(login, "login/", methods=["POST"])
    app.add_route(register, "register/", methods=["POST"])
    app.add_route(receive, "receive/", methods=["GET"])
    app.add_route(room_messages, "room/<pk>/", methods=["GET"])
    app.add_route(create_room, "room/create/", methods=["POST"])
