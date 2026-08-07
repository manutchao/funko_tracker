import threading
import requests
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineListItem, OneLineListItem
from kivymd.uix.snackbar import MDSnackbar
from kivy.app import App
from app.config import API_BASE_URL

FUNKO_ENDPOINT = f"{API_BASE_URL}/funkos"

class DatabaseView(MDBoxLayout):
    page = 1
    page_size = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.load_data(), 0)

    def load_data(self):
        if not hasattr(self.ids, "data_list"):
            Clock.schedule_once(lambda dt: self.load_data(), 0)
            return

        self.ids.data_list.clear_widgets()
        self.ids.data_list.add_widget(OneLineListItem(text="Loading Funkos..."))

        def run():
            try:
                r = requests.get(
                    FUNKO_ENDPOINT,
                    params={"page": self.page, "limit": self.page_size},
                    timeout=10,
                )
                r.raise_for_status()
                data = r.json()
                funkos = data.get("data", data)
                Clock.schedule_once(lambda dt: self.update_ui(funkos), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_error(e), 0)

        threading.Thread(target=run, daemon=True).start()

    def update_ui(self, funkos):
        self.ids.data_list.clear_widgets()
        self.ids.page_label.text = f"Page {self.page}"
        if not funkos:
            self.ids.data_list.add_widget(OneLineListItem(text="No Funkos found"))
            return
        for funko in funkos:
            item = TwoLineListItem(
                text=funko.get("name", "Unnamed Funko"),
                secondary_text=f"{funko.get('license','')} - #{funko.get('number','')}"
            )
            item.bind(on_release=lambda inst, f=funko: self.open_detail(f))
            self.ids.data_list.add_widget(item)

    def open_detail(self, funko):
        app = App.get_running_app()
        sm = app.root.ids.screen_manager
        sm.get_screen("content_item").original_data = funko
        sm.current = "content_item"

    def next_page(self):
        self.page += 1
        self.load_data()

    def previous_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_data()

    def show_error(self, error):
        MDSnackbar(text=str(error)).open()
