# config.py
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("config")

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

# Log config at DEBUG level (only shown when logging is configured)
logger.debug(f"APP_ENV = {APP_ENV}, API_BASE_URL = {API_BASE_URL}")

