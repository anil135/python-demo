#imports the SQLAlchemy class from the flask_sqlalchemy module
from flask_sqlalchemy import SQLAlchemy

#SQLAlchemy: An SQL toolkit and ORM for Python that allows developers to interact with databases using Python objects instead of SQL queries
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
