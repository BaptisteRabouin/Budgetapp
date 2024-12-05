import os
from app import db, create_app

db_path = "/app/data/app.db"

if not os.path.exists(db_path):
    print("Base de données non trouvée. Initialisation en cours...")
    os.makedirs("/app/data", exist_ok=True)
    app = create_app()
    with app.app_context():
        db.create_all()
        os.system("flask db init")
        os.system("flask db migrate")
        os.system("flask db upgrade")
else:
    print("Base de données trouvée.")
