from models import db
from config import Config
from app import app

app.config.from_object(Config)

with app.app_context():
    db.create_all()
