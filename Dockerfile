FROM python:3.12-slim

# Étape 2 : Installer les dépendances système
RUN apt-get update -y && apt-get install -y adduser && rm -rf /var/lib/apt/lists/*

# Étape 3 : Créer les répertoires nécessaires
RUN mkdir -p /app/data

# Etape 3.1 : Se place dans le répertoire de travail
WORKDIR /app

# Étape 4 : Copier uniquement les fichiers nécessaires pour installer les dépendances
COPY requirements.txt /app/

# Étape 5 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Ajoute le user appuser
RUN adduser --disabled-password --gecos "" --uid 1001 appuser 

# Donne les droits au dossier app
RUN chown -R appuser:appuser /app

# Declare le volume
VOLUME ["/app/data"]


# Swtch vers le user app
USER appuser

# Copier le reste des fichiers de l'application
COPY . /app

# Étape 6 : Exposer le port pour l'application
EXPOSE 5000

# Étape 7 : Commande pour lancer le script init_db.py au démarrage
CMD ["sh", "-c", "python init_db.py && gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app"]
