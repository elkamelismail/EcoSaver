from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS, cross_origin
from config import ApplicationConfig
from model import db, User
import geocoder

app = Flask(__name__) # create the Flask app
app.config.from_object('config.ApplicationConfig') # load the config from config.py

bcrypt = Bcrypt(app) # create the Bcrypt instance
server_session = Session(app) # create the Session instance
db.init_app(app) # initialize the SQLAlchemy instance

with app.app_context(): # create the database tables
    db.create_all()

CORS(app, supports_credentials=True) # enable CORS

#-------------------------------------------------------------------
# Authentication routes  
#-------------------------------------------------------------------

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    """
    Register a new user
    """

    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')

    user_exist = User.query.filter_by(email=email).first() is not None 

    if user_exist: # check if the user already exists
        return jsonify({
            "error": "User already exists"
        }), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # hash the password
    new_user = User(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        password=hashed_password
        ) # create the new user
    db.session.add(new_user) # add the new user to the database
    db.session.commit() # commit the changes

    return jsonify({
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email
    })

@app.route('/api/v1/auth/authenticate', methods=['POST'])
def authenticate():
    """
    Authenticate a user
    """
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    if user is None: # check if the user exists
        return jsonify({
            "error": "User does not exist"
        }), 404

    if not bcrypt.check_password_hash(user.password, password): # check if the password is correct
        return jsonify({
            "error": "Incorrect password"
        }), 401
    
    session['user_id'] = user.id # set the user id in the session

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    })

@app.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    """
    Logout a user
    """
    session.pop('user_id', None)
    return "200"

@app.route('/api/v1/auth/user', methods=['GET'])
def user():
    """
    Return the user details if the user is logged in
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            "error": "User not logged in"
        }), 401

    user = User.query.filter_by(id=session['user_id']).first()

    if user is None: # check if the user exists
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    })

#-------------------------------------------------------------------
# Location route
#-------------------------------------------------------------------

@app.route('/api/v1/location', methods=['GET'])
def get_locations():
    """
    Return the current location of the user
    """
    
    try:
        g = geocoder.ip('me')
        return jsonify({
            "city": g.city,
            "latitude": g.latlng[0],
            "longitude": g.latlng[1]
        })
    except:
        return jsonify({
            "error": "Could not get location"
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
    