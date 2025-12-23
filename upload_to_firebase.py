import json
from firebase_admin import credentials, initialize_app, db

# Configuración de Firebase
FIREBASE_CREDENTIALS = 'datagov-15614-default-rtdb-export.json'
FIREBASE_DB_URL = 'https://datagov-15614-default-rtdb.firebaseio.com/'

# Inicializar Firebase
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
initialize_app(cred, {'databaseURL': FIREBASE_DB_URL})

def upload_to_firebase(json_file):
    """Sube datos desde un archivo JSON a Firebase."""
    with open(json_file, mode='r', encoding='utf-8') as file:
        data = json.load(file)

    # Subir categorías
    category_ref = db.reference('Category')
    category_ref.set(data['Category'])

    # Subir proyectos
    projects_ref = db.reference('Projects')
    projects_ref.set(data['Projects'])

if __name__ == '__main__':
    JSON_INPUT = 'data/arequipa/inversiones_arequipa.json'

    upload_to_firebase(JSON_INPUT)
    print(f"Datos subidos a Firebase desde {JSON_INPUT}")