"""Scanner."""

import logging

from kivy.uix.boxlayout import BoxLayout
from kivy_garden.zbarcam import ZBarCam
from kivymd.uix.button import MDRaisedButton


class ScannerScreen(BoxLayout):
    """Scanner screen."""

    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        self.app = app

        # Ajouter le bouton de démarrage du scan
        scan_button = MDRaisedButton(
            text="Démarrer le scan",
            pos_hint={"center_x": 0.5},
            on_release=self.start_scan,
        )
        self.add_widget(scan_button)

        # Ajouter le layout du ZBarCam
        self.zbarcam_layout = BoxLayout(
            orientation="vertical", size_hint_y=None, height=0
        )
        self.zbarcam = ZBarCam()
        self.zbarcam_layout.add_widget(self.zbarcam)

        self.add_widget(self.zbarcam_layout)

        # Lier l'événement des symboles du scanner
        if self.app:
            self.zbarcam.bind(symbols=self.app.on_symbols)

    def start_scan(self, instance):
        """Démarre le scanner en ajustant la hauteur du layout du scanner."""
        _ = instance  # Ignorer l'argument non utilisé
        self.zbarcam_layout.height = self.height
        self.zbarcam_layout.size_hint_y = 1

    def on_start(self):
        """Log app start."""
        logging.debug("Scanner screen displayed")
