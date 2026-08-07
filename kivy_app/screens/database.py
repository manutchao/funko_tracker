import threading
import requests
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem, OneLineListItem
from kivymd.uix.snackbar import MDSnackbar
from app.config import API_BASE_URL

FUNKO_ENDPOINT = f"{API_BASE_URL}/funkos"

class DatabaseScreen(MDScreen):
    page = 1
    page_size = 7
    total = 0  # total des éléments côté serveur

    def on_enter(self):
        # Appelle le load_data une fois que la page est affichée
        Clock.schedule_once(lambda dt: self.load_data(), 0.1)

    # ===== API CALL =====
    def load_data(self):
        # Vérifie que les ids existent
        if not hasattr(self.ids, "data_list") or not hasattr(self.ids, "page_label"):
            Clock.schedule_once(lambda dt: self.load_data(), 0.1)
            return

        # Affiche "loading"
        self.ids.data_list.clear_widgets()
        self.ids.data_list.add_widget(OneLineListItem(text="Loading Funkos..."))

        def fetch():
            try:
                response = requests.get(
                    FUNKO_ENDPOINT,
                    params={"page": self.page, "limit": self.page_size},
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()

                funkos = data.get("data", [])
                self.total = data.get("total", 0)

                # Mettre à jour l'UI côté main thread
                Clock.schedule_once(lambda dt: self.update_ui(funkos), 0)

            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_error(e), 0)

        threading.Thread(target=fetch, daemon=True).start()

    # ===== UI UPDATE =====
    def update_ui(self, funkos):
        self.ids.data_list.clear_widgets()
        self.ids.page_label.text = f"Page {self.page} / {max(1, (self.total + self.page_size - 1)//self.page_size)}"

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

    # ===== PAGINATION =====
    def next_page(self):
        if self.page * self.page_size < self.total:
            self.page += 1
            self.load_data()

    def previous_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_data()

    # ===== NAVIGATION =====
    def open_detail(self, funko):
        screen = self.manager.get_screen("content_item")
        screen.original_data = funko
        self.manager.current = "content_item"

    def show_error(self, error):
        MDSnackbar(text=f"API Error: {error}").open()
