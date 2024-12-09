# Budget 🧾💰

**Budget** est une application web simple et efficace pour gérer vos budgets personnels ou familiaux. Avec une interface intuitive et des fonctionnalités adaptées, elle permet de suivre vos revenus, charges et répartitions budgétaires en toute simplicité.

L'application a été conçue avec une IA car je ne suis pas développeur de formation mais j'avais un réel besoin de pouvoir gérer facilement le budget familial

---

## Fonctionnalités 🚀

- **Création de budgets** : Ajoutez et gérez plusieurs budgets selon vos besoins.
- **Gestion des revenus et charges** : Suivez vos flux financiers avec des détails précis.
- **Répartition des contributions** : Attribuez des pourcentages de revenus à différentes personnes.
- **Visualisation et édition** : Modifiez facilement les entrées et consultez l'état de vos budgets actifs.
- **Protection par mot de passe** : Sécurisez vos données avec un accès authentifié.
- **Notifications** : Recevez des messages d'information et de confirmation pour une expérience fluide.

---

## Installation 🛠️

### Option 1 : Avec Docker (recommandée) 🐳

Une image Docker est prête à être utilisée pour faciliter le déploiement.

1. **Téléchargez et exécutez l'image Docker** :
    ```bash
    docker pull nollor/budgetapp
    docker run -d -p 80:80 --name budgetapp-container -v /votre/chemin/local/data:/app/data votre-utilisateur/budgetapp
    ```

2. **Accédez à l'application** :  
    Ouvrez un navigateur et accédez à `http://localhost:80` ou `http://<IP>:80`.
    Le mot de passe par défaut est : **password**  
    Vous pouvez le changer facilement en cliquant sur "Modifier le mot de passe" sous le bouton déconnexion. 
---

### Option 2 : Installation manuelle

1. **Clonez le projet** :
    ```bash
    git clone https://gitlab.com/Nollor/BudgetApp.git
    cd BudgetApp
    ```

2. **Configurez l'environnement** :
    - Assurez-vous d'avoir Python 3.12 ou une version compatible.
    - Créez et activez un environnement virtuel :
      ```bash
      python -m venv venv
      source venv/bin/activate  # ou .\venv\Scripts\activate sur Windows
      ```

3. **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialisez la base de données** :
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **Lancez l'application** :
    ```bash
    gunicorn -w 1 -b 0.0.0.0:80 wsgi:app 
    ```

---

## Utilisation en production 🏭

Pour un déploiement en production, l'application peut être exécutée à l'aide de **Gunicorn**. Voici les étapes générales si vous souhaitez configurer manuellement :

1. **Construisez l'image Docker (optionnel)** :
    ```bash
    docker build -t budgetapp .
    ```

2. **Exécutez le conteneur** :
    ```bash
    docker run -d -p 80:80 --name budgetapp-container -v /votre/chemin/local/data:/app/data budgetapp
    ```

---

## Captures d'écran 📸

### Interface de gestion des budgets
![Interface budgets](https://via.placeholder.com/800x400)

### Page de gestion des personnes
![Interface gestion personnes](https://via.placeholder.com/800x400)

## Auteurs ✍️

- [Nollor](https://gitlab.com/Nollor)

