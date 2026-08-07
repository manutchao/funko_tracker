# config.py
import os

# Détecte si on est sur Android (Kivy APK)
try:
    from jnius import autoclass
    ANDROID = True
except ImportError:
    ANDROID = False

# Définir l'environnement
if ANDROID:
    # Pour l'APK mobile : utiliser le serveur local/debug
    APP_ENV = "mobile"
else:
    # Sur PC / dev / prod : lire la variable d'environnement
    APP_ENV = os.environ.get("APP_ENV", "prod")  # default prod

# Définir l'URL de l'API selon l'environnement
if APP_ENV == "mobile":
    # L'IP locale de ton PC qui héberge le backend
    API_BASE_URL = "http://192.168.1.13:8000"
elif APP_ENV == "dev":
    API_BASE_URL = "http://dev.example.com"
else:
    # Production
    API_BASE_URL = "https://api.tonapp.railway.app"

# Optionnel : debug
print(f"[CONFIG] APP_ENV = {APP_ENV}, API_BASE_URL = {API_BASE_URL}")
