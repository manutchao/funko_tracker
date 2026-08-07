import threading
import logging
from typing import List, Dict, Any

import requests
from kivy.clock import Clock
from kivy.utils import platform
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar


logger = logging.getLogger("SaisieManuelleScreen")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


# Permissions Android
if platform == "android":
    from android.permissions import Permission, request_permissions

    request_permissions(
        [
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.CAMERA,
        ]
    )

API_BASE_URL = "http://192.168.1.13:8000"
FUNKO_ENDPOINT = f"{API_BASE_URL}/funkos/"


class SaisieManuelleScreen(MDScreen):
    """
    Kivy screen for manual Funko entry.

    Provides a form with field validation,
    sends data to the API, and redirects
    to the home screen after a successful submission.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the screen and error dialog.

        :param kwargs: Additional arguments for MDScreen
        """
        super().__init__(**kwargs)
        self.dialog = None

    def validate_form(self) -> None:
        """
        Validate the form ensuring all fields are filled.
        If there are errors, they are displayed in a dialog;
        otherwise, the form is processed.
        """
        errors = []

        libelle = self.ids.field_name.text
        licence = self.ids.field_license.text
        barcode = self.ids.field_barcode.text
        number = self.ids.field_number.text

        if not libelle:
            errors.append("Le champ libellé ne peut pas être vide.")
        if not licence:
            errors.append("Le champ licence ne peut pas être vide.")
        if not barcode:
            errors.append("Le champ code-barre ne peut pas être vide.")
        if not number:
            errors.append("Le champ numéro ne peut pas être vide.")

        if errors:
            self.show_errors(errors)
        else:
            self.process_form()

    def show_errors(self, errors: List[str]) -> None:
        """
        Display a dialog with the list of validation errors.

        :param errors: List of error messages to display
        """
        error_message = "\n".join(errors)

        btn_ok = MDRaisedButton()
        btn_ok.text = "OK"
        btn_ok.bind(on_release=lambda x: self.dialog.dismiss())

        self.dialog = MDDialog(
            title="Erreurs de validation", text=error_message, buttons=[btn_ok]
        )
        self.dialog.open()
        logger.warning("Form validation errors: %s", error_message)


    def process_form(self) -> None:
        """
        Prepare the form payload and send it to the API.
        Display a success or error message depending on the response.
        """
        payload = {
            "name": self.ids.field_name.text,
            "license": self.ids.field_license.text,
            "barcode": self.ids.field_barcode.text,
            "number": self.ids.field_number.text,
        }

        logger.info("Form successfully validated with payload: %s", payload)
        self.post_funko(payload)

    def post_funko(self, payload: Dict[str, str]) -> None:
        """
        Send the form payload to the API in a separate thread
        to avoid blocking the UI.

        :param payload: Form data to send
        """

        def run():
            try:
                response = requests.post(FUNKO_ENDPOINT, json=payload, timeout=10)
                if response.status_code in (200, 201):

                    def show_snackbar(dt):
                        snackbar = MDSnackbar()
                        snackbar.text = "Funko ajoutée 🎉"
                        snackbar.open()

                    Clock.schedule_once(show_snackbar, 0)
                    Clock.schedule_once(self.redirect_to_home, 1)
                    logger.info("Funko successfully added. API response: %s", response.status_code)
                else:

                    def show_error(dt):
                        snackbar = MDSnackbar()
                        snackbar.text = f"Erreur API ({response.status_code})"
                        snackbar.open()

                    Clock.schedule_once(show_error, 0)
                    logger.error("API error: %s", response.status_code)
            except requests.exceptions.RequestException as e:

                def show_request_error(dt):
                    snackbar = MDSnackbar()
                    snackbar.text = f"Erreur API: {e}"
                    snackbar.open()

                Clock.schedule_once(show_request_error, 0)
                logger.exception("API request exception: %s", e)

        threading.Thread(target=run, daemon=True).start()

    def redirect_to_home(self, *_: Any) -> None:
        """
        Redirect the user to the home screen.

        :param _: Optional Kivy Clock parameters (not used)
        """
        self.manager.current = "accueil"
        logger.info("Redirected to home screen")
