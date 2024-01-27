from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# DB will be used for db queries via SQLAlchemy 
db = SQLAlchemy()
ma = Marshmallow()

def create_table(my_app):
        try:
                with my_app.app_context():
                    db.create_all()
                    print("Users table created.")
        except:
                print("Users table could not created.")