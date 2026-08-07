# Build APK pour debug sur PC (simulateur)
debug_on_local:
	@echo "Debug on local PC"
	APP_ENV=dev pipenv run buildozer -v android debug

# Build APK pour test sur téléphone
debug_on_phone:
	@echo "Debug on phone (Android)"
	APP_ENV=mobile pipenv run buildozer -v android debug deploy run logcat

# Build APK sans déployer (production ou test)
build_package:
	pipenv run buildozer -v android debug

# Nettoyage Buildozer
buildozer_clean:
	buildozer android clean

# Supprimer l'environnement virtuel
delete_venv:
	pipenv --rm

# Lancer API localement
launch_api_local:
	pipenv run uvicorn app.main:app --host 0.0.0.0 --port 8000

launch_api_phone:
	APP_ENV=mobile pipenv run uvicorn app.main:app --host 0.0.0.0 --port 8000
