from db.session import ma

class UserSchema(ma.Schema):
      class Meta:
            fields = ('userid', 'username', 'email', 'passwd', 'last_login')

user_schema = UserSchema()
users_schema = UserSchema(many=True)