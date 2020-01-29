from database import DB
from user import User

class Advertisement:
    def __init__(self, id, title, description, price, date, active, buyer_id, seller_id):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.date = date
        self.active = active
        self.buyer_id = buyer_id
        self.seller_id = seller_id

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM advertisements').fetchall()
            return [Advertisement(*row) for row in rows]

    @staticmethod
    def sold_ads(id):
        with DB() as db:
            values = (id,)
            rows = db.execute('SELECT * FROM advertisements WHERE seller_id = ? AND active = 0', values).fetchall()
            return [Advertisement(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM advertisements WHERE id = ?',
                (id,)
            ).fetchone()
            return Advertisement(*row)

    @staticmethod
    def find_by_seller_id(seller_id):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM advertisements WHERE seller_id = ?',
                (seller_id,)
            ).fetchall()
            return [Advertisement(*row) for row in rows]

    @staticmethod
    def seller_name_by_id(seller_id):
        with DB() as db:
            name = db.execute(
                'SELECT name FROM users WHERE id = ?',
                (seller_id,)
            ).fetchone()
            return name[0]

    @staticmethod
    def buyer_name_by_id(buyer_id):
        with DB() as db:
            name = db.execute(
                'SELECT name FROM users WHERE id = ?',
                (buyer_id,)
            ).fetchone()
            return name[0]

    @staticmethod
    def buyer_info_by_id(buyer_id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE id = ?',
                (buyer_id,)
            ).fetchone()
            return User(*row)       


    def create(self):
        with DB() as db:
            values = (self.title, self.description, self.price, self.date, self.active, self.buyer_id, self.seller_id)
            db.execute('''
                INSERT INTO advertisements (title, description, price, date, active, buyer_id, seller_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    def buy(self, buyer_id):
        with DB() as db:
            values = (buyer_id, self.id)
            db.execute('''UPDATE advertisements SET active = 0, buyer_id = ? WHERE id = ?''', values)
            self.active = 0
            self.buyer_id = buyer_id
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM advertisements WHERE id = ?', (self.id,))

    def save(self):
        with DB() as db:
            values = (
                self.title,
                self.description,
                self.price,
                self.date,
                self.id
            )
            db.execute(
                '''UPDATE advertisements
                SET title = ?, description = ?, price = ?, date = ?
                WHERE id = ?''', values)
            return self