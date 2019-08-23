from app.database import DB as models


class UserRoom(models.Model):
    __tablename__ = "user_room"
    user = models.Column(None, models.ForeignKey("users.id"), nullable=False)
    room = models.Column(None, models.ForeignKey("rooms.id"), nullable=False)


class Room(models.Model):
    __tablename__ = "rooms"
    relations = ("messages", )

    id = models.Column(models.Integer, primary_key=True)
    title = models.Column(models.String, nullable=False)


class Message(models.Model):
    __tablename__ = "messages"

    id = models.Column(models.Integer, primary_key=True)
    message = models.Column(models.String, nullable=False)
    room = models.Column(None, models.ForeignKey("rooms.id"), nullable=False)
    from_user = models.Column(None, models.ForeignKey("users.id"), nullable=False)
    created_at = models.Column(models.DateTime(), server_default="now()")
