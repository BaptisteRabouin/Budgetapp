from . import db
from datetime import datetime

class Charge(db.Model):
    __tablename__ = 'charges'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)

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
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)

    def is_consistent(self):
        """Vérifie si le budget de la personne correspond au budget du revenu."""
        if self.person_id and self.person.budget_id != self.budget_id:
            return False
        return True

    def __repr__(self):
        return f'<Revenue {self.description} - {self.amount}>'

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    allocation_percentage = db.Column(db.Float, nullable=False, default=50.0)  # Pourcentage alloué par défaut
    revenues = db.relationship('Revenue', back_populates='person')  # Relation avec les revenus
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)

    def __repr__(self):
        return f'<Person {self.name} - {self.allocation_percentage}%>'


    def can_be_deleted(self):
        """Retourne True si la personne n'a pas de revenus associés."""
        return len(self.revenues) == 0



class Budget(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    charges = db.relationship('Charge', backref='budget', lazy=True)
    revenues = db.relationship('Revenue', backref='budget', lazy=True)
    persons = db.relationship('Person', backref='budget', lazy=True)

    def __repr__(self):
        return f'<Budget {self.name}>'

    
    def get_persons(self):
        """Récupère toutes les personnes associées à ce budget."""
        return Person.query.filter_by(budget_id=self.id).all()

    def get_revenues(self):
        """Récupère tous les revenus associés à ce budget."""
        return Revenue.query.filter_by(budget_id=self.id).all()
