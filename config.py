import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '123456abcdef'  # à changer pour une clé secrète sécurisée
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_PASSWORD = 'password'  # Définir le mot de passe ici
