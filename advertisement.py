from database import DB

class Advertisement:
    def __init__(self, id, title, description, price, date, active, buyer_id, seller_id):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.date = date
        self.actice = active
        self.buyer_id = buyer_id
        self.seller_id = seller_id

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM advertisements').fetchall()
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
                'SELECT name FROM users WHERE seller_id = ?',
                (seller_id,)
            ).fetchone()
            return name


    def create(self):
        with DB() as db:
            values = (self.title, self.description, self.price, self.date, 1, 0, self.seller_id)
            db.execute('''
                INSERT INTO advertisements (title, description, price, date, active, buyer_id, seller_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    