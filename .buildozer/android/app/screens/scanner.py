"""Scanner screen.""" ""
import logging

from kivy.lang import Builder
from kivy_garden.zbarcam import ZBarCam
from kivymd.uix.screen import MDScreen


class ScannerScreen(MDScreen):
    """Scanner screen.""" ""

    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        if self.app:
            self.ids.zbarcam.bind(symbols=self.app.on_symbols)

    def start_scan(self, instance):
        """Démarre le scanner en ajustant la hauteur du layout du scanner."""
        _ = instance  # Ignorer l'argument non utilisé
        self.ids.zbarcam_layout.height = self.height
        self.ids.zbarcam_layout.size_hint_y = 1

    def on_start(self):
        """Log app start."""
        logging.debug("Scanner start")
