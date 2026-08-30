import logging
import os

os.environ["KIVY_NO_CONFIG"] = "1"

from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp

from screens.accueil import AccueilScreen
from screens.content_item import ContentItemScreen
from screens.database import DatabaseScreen
from screens.saisie_manuelle import SaisieManuelleScreen
from screens.scanner import ScannerScreen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "kv")


class MainApp(MDApp):
    """App."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Funko Tracker"

    def build(self):
        """Build app."""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Brown"

        Builder.load_file(os.path.join(KV_DIR, "accueil.kv"))
        Builder.load_file(os.path.join(KV_DIR, "database.kv"))
        Builder.load_file(os.path.join(KV_DIR, "saisie_manuelle.kv"))
        Builder.load_file(os.path.join(KV_DIR, "scanner.kv"))
        Builder.load_file(os.path.join(KV_DIR, "content_item.kv"))

        root = Builder.load_file(os.path.join(KV_DIR, "main.kv"))

        for widget in root.walk():
            if isinstance(widget, ScreenManager):
                widget.transition = NoTransition()

        return root

    def on_start(self):
        """Log app start."""
        logging.debug("App has started")

    def on_symbols(self, instance, symbols):
        """
        Callback for barcode scan event from ZBarCam.
        Receives a list of detected barcodes and navigates to database screen.
        """
        if not symbols:
            return

        barcode = symbols[0]
        barcode_value = barcode.get("decoded") or str(barcode)
        logging.info(f"Barcode scanned: {barcode_value}")

        root = self.root
        if root:
            root.current = "database"
            database_screen = root.get_screen("database")
            if database_screen and hasattr(database_screen, "search_by_barcode"):
                database_screen.search_by_barcode(barcode_value)


if __name__ == "__main__":
    MainApp().run()
