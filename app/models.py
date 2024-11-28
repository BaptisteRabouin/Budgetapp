from . import db

class Charge(db.Model):
    __tablename__ = 'charges'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Charge {self.description} - {self.amount}>'

class Revenue(db.Model):
    __tablename__ = 'revenues'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Revenue {self.description} - {self.amount}>'
