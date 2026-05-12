from app import app
from models import User

with app.app_context():
    admin = User.query.filter_by(email="admin@helpdesk.com").first()

    if admin:
        print(admin.username, admin.role)
    else:
        print("Admin not found")