import flask
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os, json
from flask_marshmallow import Marshmallow
from datetime import datetime
#from src.models.user_model import User
#from api.users_route import user_route

# app creation
my_app = Flask(__name__)
my_app.secret_key = '\xaae\xcb\xcb\xe7\x1d\x01a\x89\xb1o8\xd0y\xfa\xdf\xed\x12\x9e\x985\x10KY'
#  Load all key=value pairs into the app
load_dotenv()

my_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_URI')
my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(my_app)
ma = Marshmallow(my_app)

class User(db.Model):
      __tablename__ = 'Users'

      userid = db.Column(db.Integer, primary_key=True, index=True)
      username = db.Column(db.String(100), unique = True)
      email = db.Column(db.String(80), unique = True)
      passwd = db.Column(db.String(80))
      last_login = db.Column(db.DateTime)

      def __init__(self, userid, username, email, passwd, last_login):
            self.userid = userid
            self.username = username
            self.email = email
            self.passwd = passwd
            self.last_login = last_login
      
      def create_table():
            try:
                  with my_app.app_context():
                        db.create_all()
                        print("Users table created.")
            except:
                  print("Users table could not created.")

class UserSchema(ma.Schema):
      class Meta:
            fields = ('userid', 'username', 'email', 'passwd', 'last_login')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#my_app.register_blueprint(user_route)

@my_app.route('/api/users/create',  methods = ['POST'])
def api_create_user():
      user = request.get_json()

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
            return make_response({'message': 'User already exists!'}, 409)
      else:
            db.session.add(new_user)
            db.session.commit()

            return make_response({'message': 'succesfully inserted'}, 200)

@my_app.route('/api/users',  methods = ['GET'])
def api_get_users():
      users = User.query.all()
      return users_schema.jsonify(users)


@my_app.route('/api/users/<id>',  methods = ['GET', 'PUT', 'DELETE'])
def api_update_user(id):
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

@my_app.route('/api/users/login',  methods = ['POST'])
def api_login():
      email = request.json['email']
      passwd = request.json['passwd']

      print(f"{email}, {passwd}")

      if  not email or not passwd:
            return make_response({'message': 'Please, add e-mail and password!'}, 404)

      # return None if not found
      if User.query.filter_by(email = email).first() and User.query.filter_by(passwd = passwd).first():
            return make_response({'message': 'User credentials are valid'}, 200)
      else:
            return make_response({'message': 'User credentials are incorrect!'}, 404)

if __name__ == "__main__":
        # user table creation in MySQL DB
        User.create_table()
        my_app.run(host='0.0.0.0', port=8888, debug=True)