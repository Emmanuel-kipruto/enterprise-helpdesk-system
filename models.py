from datetime import datetime
from extensions import db
from flask_login import UserMixin


# --------------------
# USER MODEL
# --------------------
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )


# --------------------
# TICKET MODEL
# --------------------
class Ticket(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    ticket_code = db.Column(
        db.String(20),
        unique=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Low"
    )

    status = db.Column(
        db.String(20),
        default="Open"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    technician = db.Column(
        db.String(100),
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )