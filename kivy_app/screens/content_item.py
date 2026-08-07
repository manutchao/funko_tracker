from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import requests
from app.config import API_BASE_URL


class ContentItemScreen(MDScreen):
    edit_mode = False
    original_data = None  # Données de la Funko

    def on_pre_enter(self, *args):
        if self.original_data:
            Clock.schedule_once(self.fill_fields, 0.1)

    def fill_fields(self, dt):
        data = self.original_data
        if not data:
            return

        self.ids.field_name.text = data.get("name", "")
        self.ids.field_license.text = data.get("license", "")
        self.ids.field_barcode.text = data.get("barcode", "")
        self.ids.field_number.text = str(data.get("number", ""))

        self.set_fields_readonly(not self.edit_mode)

    def set_fields_readonly(self, readonly: bool):
        """Active/désactive tous les champs."""
        for field_id in ["field_name", "field_license", "field_barcode", "field_number"]:
            self.ids[field_id].disabled = readonly

    def edit_item(self):
        """Active le mode édition et scroll/focus sur le premier champ."""
        self.edit_mode = True
        self.set_fields_readonly(False)

        def focus_first_field(dt):
            field = self.ids.field_name
            scrollview = self.ids.scroll_fields  # ton ScrollView contenant les champs
            field.focus = True
            scrollview.scroll_to(field)

        Clock.schedule_once(focus_first_field, 0.2)
        self.ids.edit_button.text = "Enregistrer"

    def save_item(self):
        """Envoie les modifications à FastAPI PATCH."""
        if not self.original_data or "_id" not in self.original_data:
            self.show_snackbar("Impossible de sauvegarder : ID manquant")
            return

        # Extraire le MongoDB ObjectId
        _id = self.original_data["_id"]
        funko_id = _id["$oid"] if isinstance(_id, dict) and "$oid" in _id else str(_id)

        try:
            number_value = int(self.ids.field_number.text)
        except ValueError:
            self.show_snackbar("Le numéro doit être un entier")
            return

        payload = {
            "name": self.ids.field_name.text,
            "license": self.ids.field_license.text,
            "barcode": self.ids.field_barcode.text,
            "number": number_value,
        }

        try:
            # PATCH vers FastAPI, sans slash final
            response = requests.patch(
                f"{API_BASE_URL}/funkos/{funko_id}",
                json=payload,
                timeout=10
            )
            response.raise_for_status()  # lève une exception si code >= 400
            self.original_data.update(payload)

            self.edit_mode = False
            self.set_fields_readonly(True)
            self.ids.edit_button.text = "Modifier"
            self.show_snackbar("Funko mise à jour 🎉")

        except requests.RequestException as e:
            self.show_snackbar(f"Erreur lors de la sauvegarde : {e}")

    def delete_item(self):
        """Supprime la Funko après confirmation."""
        if not self.original_data or "_id" not in self.original_data:
            self.show_snackbar("Impossible de supprimer : ID manquant")
            return

        _id = self.original_data["_id"]
        funko_id = _id["$oid"] if isinstance(_id, dict) and "$oid" in _id else str(_id)

        def confirm_delete(*args):
            try:
                response = requests.delete(f"{API_BASE_URL}/funkos/{funko_id}", timeout=10)
                response.raise_for_status()
                self.show_snackbar("Funko supprimée 🗑️")
                self.manager.current = "database"
            except requests.RequestException as e:
                self.show_snackbar(f"Erreur lors de la suppression : {e}")

        dialog = MDDialog(
            title="Confirmer la suppression",
            text="Voulez-vous vraiment supprimer cette Funko ?",
            buttons=[
                MDFlatButton(text="Annuler"),
                MDFlatButton(text="Supprimer", on_release=lambda x: (confirm_delete(), dialog.dismiss())),
            ],
        )
        dialog.open()

    def show_snackbar(self, message: str):
        snackbar = MDSnackbar()
        snackbar.text = message
        snackbar.open()
