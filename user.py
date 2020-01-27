import hashlib
from database import DB

class User:
    def __init__(self, id, email, password, name, address, mobile):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.mobile = mobile

    def create(self):
    	with DB() as db:
       		values = (self.email, self.password, self.name, 
            	self.address, self.mobile)
        	db.execute('''
            	INSERT INTO users (email, password, name, address, mobile)
            	VALUES (?, ?, ?, ?, ?)''', values)
        	return self
            
    @staticmethod
    def hashPassword(password):
		return hashlib.sha256(password.encode('utf-8')).hexdigest()
