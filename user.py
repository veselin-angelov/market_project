import hashlib
from database import DB

from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
    )

SECRET_KEY = "SxOW8IKSGVShQD6BXtQzMA"

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
    def find(email):
        if not email:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE email = ?',(email,)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def find_name_by_id(id):
        with DB() as db:
            name = db.execute(
                'SELECT name FROM users WHERE id = ?',(id,)
            ).fetchone()
            return name[0]

    @staticmethod
    def hashPassword(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verifyPassword(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

    def generateToken(self):
        s = Serializer(SECRET_KEY, expires_in=600)
        return s.dumps({'email': self.email})

    @staticmethod
    def verifyToken(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True
