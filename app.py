# Imports necessary Libraries and modules
from flask import Flask, request, jsonify
from models import db, User
from config import Config

#The Flask app is created and configured
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

#The database is initialized with the app context
#A function to create database tables before the first request is made
#Two endpoints are defined for creating and retrieving users.
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

#The application is set to run on a specified host and port.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
