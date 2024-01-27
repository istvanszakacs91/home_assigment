from db.session import db

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