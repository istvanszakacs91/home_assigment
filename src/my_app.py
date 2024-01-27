from flask import Flask
from dotenv import load_dotenv
import os
from db.session import db, create_table
from api.users_route import user_route

# app creation
my_app = Flask(__name__)
my_app.secret_key = '\xaae\xcb\xcb\xe7\x1d\x01a\x89\xb1o8\xd0y\xfa\xdf\xed\x12\x9e\x985\x10KY'
#  Load all key=value pairs into the app
load_dotenv()

my_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_URI')
my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object with your Flask app
db.init_app(my_app)

print(my_app)
my_app.register_blueprint(user_route)

if __name__ == "__main__":
        # user table creation in MySQL DB
        create_table(my_app)
        my_app.run(host='0.0.0.0', port=8888, debug=True)