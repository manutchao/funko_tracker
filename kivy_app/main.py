import os
os.environ["KIVY_NO_CONFIG"] = "1"

from kivymd.app import MDApp


import logging
import os
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from screens.accueil import AccueilScreen
from screens.content_item import ContentItemScreen
from screens.database import DatabaseScreen
from screens.saisie_manuelle import SaisieManuelleScreen
from screens.scanner import ScannerScreen

# Window.size = (400, 800)  # Largeur, Hauteur

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "kv")


class MyScreenManager(ScreenManager):
    """Screen Manager."""


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
        return Builder.load_file(os.path.join(KV_DIR, "main.kv"))


    def on_start(self):
        """Log app start."""
        logging.debug("App has started")


if __name__ == "__main__":
    MainApp().run()


