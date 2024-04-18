from db import db


class TasksModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(80), nullable = False)
