"""Main screen."""

# from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDTopAppBar

from screens.add_screen import AddScreen
from screens.scanner_screen import ScannerScreen


class MainScreen(Screen):
    """Main screen."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.setup_layout()
        self.data_list = MDList()

    def set_app(self, app):
        """Initialize the application and bind scanner events."""
        self.app = app
        if self.app:
            self.update_scanner_screen()

    def update_scanner_screen(self):
        """Update ScannerScreen with the application instance."""
        if self.app and self.ids.get("scanner_screen"):
            self.ids.scanner_screen.app = self.app

    def setup_layout(self):
        """Configure the main layout and UI elements."""
        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(self.create_toolbar())
        main_layout.add_widget(self.create_bottom_navigation())
        self.add_widget(main_layout)

    def create_toolbar(self):
        """Create the top toolbar."""
        toolbar = MDTopAppBar(title="Example App")
        toolbar.right_action_items = [
            ["magnify", lambda x: self.on_search_button_press()]
        ]
        return toolbar

    def create_bottom_navigation(self):
        """Create the bottom navigation with four tabs."""
        bottom_navigation = MDBottomNavigation()
        bottom_navigation.add_widget(self.create_home_tab())
        bottom_navigation.add_widget(self.create_database_tab())
        bottom_navigation.add_widget(self.create_manual_entry_tab())
        bottom_navigation.add_widget(self.create_scanner_tab())
        return bottom_navigation

    def create_home_tab(self):
        """Create the home tab."""
        return MDBottomNavigationItem(name="Accueil", text="Accueil", icon="home")

    def create_database_tab(self):
        """Create the database tab."""
        item = MDBottomNavigationItem(
            name="Base de données", text="Base de données", icon="database"
        )
        scroll_view = ScrollView()
        scroll_view.add_widget(self.data_list)
        item.add_widget(scroll_view)
        item.bind(on_tab_press=self.on_database_tab_press)
        return item

    def create_manual_entry_tab(self):
        """Create the manual entry tab."""
        item = MDBottomNavigationItem(
            name="Saisie manuelle", text="Saisie manuelle", icon="pen"
        )
        add_screen = AddScreen(app=self.app)
        item.add_widget(add_screen)
        return item

    def create_scanner_tab(self):
        """Create the scanner tab."""
        item = MDBottomNavigationItem(
            name="Scanner", text="Scanner", icon="barcode-scan"
        )
        scanner_screen = ScannerScreen()
        item.add_widget(scanner_screen)
        self.ids["scanner_screen"] = scanner_screen
        return item

    def on_database_tab_press(self, instance):
        """Populate the list with data when the database tab is selected."""
        _ = instance  # Ignorer l'argument non utilisé

        if not self.app:
            return
        data = self.app.load_json_data()
        self.data_list.clear_widgets()
        for item in data:
            elem = OneLineListItem(text=str(item))
            elem.bind(on_release=self.on_item_click)
            self.data_list.add_widget(elem)

    def on_item_click(self, instance):
        """Show the detail screen when an item is clicked."""
        if self.app:
            self.app.show_detail_screen(instance.text)

    def on_search_button_press(self):
        """Handle the search button press."""
        print("Search button pressed")


# # Charger le fichier KV
# Builder.load_file("kv/main_screen.kv")


# class MainScreen(Screen):
#     def __init__(self, **kwargs):
#         super(MainScreen, self).__init__(**kwargs)
#         self.app = None  # Initialisation de l'attribut app

#     def set_app(self, app):
#         """Initialise l'application et lie les événements du scanner."""
#         self.app = app
#         self.zbarcam.bind(symbols=self.app.on_symbols)

#     def on_kv_post(self, base_widget):
#         """Configure l'interface utilisateur après le chargement du KV."""
#         self.setup_layout()

#     def setup_layout(self):
#         main_layout = BoxLayout(orientation="vertical")
#         main_layout.add_widget(self.create_toolbar())
#         main_layout.add_widget(self.create_bottom_navigation())
#         self.add_widget(main_layout)

#     def create_toolbar(self):
#         """Crée la barre d'outils."""
#         toolbar = MDTopAppBar(title="Example App")
#         toolbar.right_action_items = [
#             ["magnify", lambda x: self.on_search_button_press()]
#         ]
#         return toolbar

#     def create_bottom_navigation(self):
#         """Crée la navigation inférieure avec trois onglets."""
#         bottom_navigation = MDBottomNavigation()
#         bottom_navigation.add_widget(self.create_home_tab())
#         bottom_navigation.add_widget(self.create_database_tab())
#         bottom_navigation.add_widget(self.create_manual_entry_tab())
#         bottom_navigation.add_widget(self.create_scanner_tab())

#         return bottom_navigation

#     def create_database_tab(self):
#         """Crée l'onglet de la base de données."""
#         item = MDBottomNavigationItem(
#             name="Base de données", text="Base de données", icon="database"
#         )
#         self.data_list = MDList()
#         scroll_view = ScrollView()
#         scroll_view.add_widget(self.data_list)
#         item.add_widget(scroll_view)
#         item.bind(on_tab_press=self.on_database_tab_press)
#         return item

#     def create_manual_entry_tab(self):
#         """Crée l'onglet de saisie manuelle."""
#         return MDBottomNavigationItem(
#             name="Saisie manuelle", text="Saisie manuelle", icon="pen"
#         )

#     def create_home_tab(self):
#         return MDBottomNavigationItem(name="Accueil", text="Accueil", icon="home")

#     def create_scanner_tab(self):
#         """Crée l'onglet du scanner."""
#         item = MDBottomNavigationItem(
#             name="Scanner", text="Scanner", icon="barcode-scan"
#         )
#         self.scanner_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

#         scan_button = MDRaisedButton(
#             text="Démarrer le scan",
#             pos_hint={"center_x": 0.5},
#             on_release=self.start_scan,
#         )
#         self.scanner_layout.add_widget(scan_button)

#         self.zbarcam_layout = BoxLayout(
#             orientation="vertical", size_hint_y=None, height=0
#         )
#         self.zbarcam = ZBarCam()
#         self.zbarcam_layout.add_widget(self.zbarcam)

#         self.scanner_layout.add_widget(self.zbarcam_layout)
#         item.add_widget(self.scanner_layout)

#         return item

#     def on_database_tab_press(self, instance):
#         """Fill database with data when database menu is selectionned"""
#         data = self.app.load_json_data()
#         self.data_list.clear_widgets()
#         for item in data:
#             elem = OneLineListItem(text=str(item))
#             elem.bind(on_release=self.on_item_click)
#             self.data_list.add_widget(elem)

#     def on_item_click(self, instance):
#         """Affiche l'écran de détail lorsqu'un élément est cliqué."""
#         self.app.show_detail_screen(instance.text)

#     def on_search_button_press(self):
#         """Gère l'appui sur le bouton de recherche."""
#         print("Search button pressed")

#     def start_scan(self, instance):
#         """Démarre le scanner en ajustant la hauteur du layout du scanner."""
#         self.zbarcam_layout.height = self.scanner_layout.height
#         self.zbarcam_layout.size_hint_y = 1
