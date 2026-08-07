"""Capture a screenshot of the saisie screen for visual preview."""
import os

os.environ["KIVY_NO_CONFIG"] = "1"

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "kv")
OUTPUT = os.path.join(BASE_DIR, "saisie_preview.png")


class SaisieManuelleScreen(MDScreen):
    def validate_form(self):
        pass


class PreviewApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Brown"
        Window.size = (400, 800)
        Builder.load_file(os.path.join(KV_DIR, "saisie_manuelle.kv"))
        return SaisieManuelleScreen()


def capture_screenshot(_dt):
    Window.export_to_png(OUTPUT)
    print(f"Screenshot saved to {OUTPUT}")
    App.get_running_app().stop()


if __name__ == "__main__":
    app = PreviewApp()
    Clock.schedule_once(capture_screenshot, 1.5)
    app.run()
