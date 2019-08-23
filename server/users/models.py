from app.database import DB as models


__all__ = ("User", )


class User(models.Model):
    __tablename__ = "users"

    id = models.Column(models.Integer, primary_key=True)
    username = models.Column(models.Unicode(100), nullable=False)
    password = models.Column(models.Unicode(100), nullable=False)
    is_active = models.Column(models.Boolean, default=False)

    def to_dict(self):
        return {"user_id": self.id, "username": self.username}

    def is_authenticated(self):
        return True
