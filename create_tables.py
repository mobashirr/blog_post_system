#creating a table for app
from application import app, db


with app.app_context():
    db.create_all()
