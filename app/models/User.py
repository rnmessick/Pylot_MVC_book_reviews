from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create(self, info):
        message = []
        if info['password'] != info['confirm_password']:
            message.append('Passwords do not match')
        if message:
            return {'status':False, 'message': message}
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
            create_user_query = "INSERT INTO users (name, alias, email, password,created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(info['name'], info['alias'], info['email'],pw_hash)
            self.db.query_db(create_user_query)
            return {'status':True}

    def login(self, info):
        login_query = "SELECT * FROM users WHERE email = '{}'".format(info['login_email'])
        login_status = self.db.query_db(login_query)
        print login_status
        if login_status[0]:
            if self.bcrypt.check_password_hash(login_status[0]['password'], info['login_password']):
                return  {
                            'status':True, 
                            'login_status':login_status[0]
                        }
            else:
                return  {
                            'status':False
                        }

    def user_info(self, user_id):
        user_id_query = "SELECT * FROM users WHERE id = {}".format(user_id)
        user = self.db.query_db(user_id_query)
        return user[0]