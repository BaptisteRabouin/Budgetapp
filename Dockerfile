# Étape 1 : Image de base
FROM python:3.12-slim

# Étape 2 : Installer les dépendances système
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential libpq-dev

# Étape 3 : Créer les répertoires nécessaires
RUN mkdir -p /app/data
WORKDIR /app

# Étape 4 : Copier les fichiers de l'application
COPY . /app

# Étape 5 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 6 : Exposer le port pour l'application
EXPOSE 5000

# Étape 7 : Commande pour lancer le script init_db.py au démarrage
CMD ["sh", "-c", "python init_db.py && gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app"]
