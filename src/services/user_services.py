from models.User import User
from models.UserSchema import user_schema, users_schema
from db.session import db
from flask import request, make_response
import flask

def create_user(user):
    userid = user['userid']
    username = user['username']
    email = user['email']
    passwd = user['passwd']
    last_login = user['last_login']

    new_user = User(userid=userid, username=username, email=email,
                passwd=passwd, last_login=last_login)

    # Check if user already exists
    user = db.session.get(User, userid)

    if user:
        return make_response({'message': 'UserID already exists!'}, 409)
    else:
        db.session.add(new_user)
        db.session.commit()

        return make_response({'message': 'succesfully inserted'}, 200)
    
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

def manage_user(id):
    user = db.session.get(User, id)
    # If user not exists
    if not user:
        return make_response({'message': 'User not found!'}, 404)
    else:
        # Update user
        if flask.request.method == 'PUT':   
                userid = request.json['userid']
                username = request.json['username']
                email = request.json['email']
                passwd = request.json['passwd']
                last_login = request.json['last_login']

                user.userid = userid
                user.username = username
                user.email = email
                user.passwd = passwd
                user.last_login = last_login

                db.session.commit()

                return user_schema.jsonify(user)
        # Remove user
        elif flask.request.method == 'DELETE':
                db.session.delete(user)
                db.session.commit()

                return user_schema.jsonify(user)
        
        # GET request, show the user data
        else:
                return user_schema.jsonify(user)
        
def login_check(email, passwd):
    if  not email or not passwd:
                return make_response({'message': 'Please, add e-mail and password!'}, 404)

    # return None if not found
    if User.query.filter_by(email = email).first() and User.query.filter_by(passwd = passwd).first():
            return make_response({'message': 'User credentials are valid'}, 200)
    else:
            return make_response({'message': 'User credentials are incorrect!'}, 404)