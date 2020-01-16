from database import DB
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, name, address, mobile):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.mobile = mobile

    def create(self):
        with DB() as db:
            values = (self.email, self.password, self.name = name, 
                self.address = address, self.mobile = mobile)
            db.execute('''
                INSERT INTO users (email, password, name, address, mobile)
                VALUES (?, ?, ?, ?, ?)''', values)
            return self