from flask import Blueprint, request
from services.user_services import create_user, get_users, manage_user, login_check

user_route = Blueprint('users_route', __name__)

# API for creating new user
@user_route.route('/api/users/create',  methods = ['POST'])
def api_create_user():
        user = request.get_json()
        return create_user(user)

@user_route.route('/api/users',  methods = ['GET'])
def api_get_users():
        return get_users()


@user_route.route('/api/users/<id>',  methods = ['GET', 'PUT', 'DELETE'])
def api_manage_user(id):
      return manage_user(id)

@user_route.route('/api/users/login',  methods = ['POST'])
def api_login_check():
        email = request.json['email']
        passwd = request.json['passwd']
        return login_check(email, passwd)