from app import app
from extensions import db
from models import User, Ticket

with app.app_context():
    db.drop_all()     # 🔥 removes ALL old broken tables
    db.create_all()   # 🔥 rebuilds fresh schema from models

    print("Database fully reset and recreated successfully!")