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
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)  # Lien avec Person

    person = db.relationship('Person', back_populates='revenues')  # Relation inverse

    def __repr__(self):
        return f'<Revenue {self.description} - {self.amount}>'

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    allocation_percentage = db.Column(db.Float, nullable=False, default=50.0)  # Pourcentage alloué par défaut

    revenues = db.relationship('Revenue', back_populates='person')  # Relation avec les revenus

    def __repr__(self):
        return f'<Person {self.name} - {self.allocation_percentage}%>'
