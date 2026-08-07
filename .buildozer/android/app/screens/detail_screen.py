"""Detail screen."""

from kivy.lang import Builder

# from kivy.metrics import dp
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.slider import Slider
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.button import MDIconButton, MDRoundFlatIconButton
# from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen

# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.toolbar import MDTopAppBar

Builder.load_file("kv/detail_screen.kv")


class DetailScreen(Screen):
    """Detail screen."""

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

    def update_screen(self, element):
        """Update."""

    def submit(self):
        """Submit."""

    def reset(self):
        """Reset."""

    #     detail_toolbar = MDTopAppBar(
    #         title="Detail",
    #         left_action_items=[["arrow-left", lambda x: self.app.show_main_screen()]],
    #         right_action_items=[["delete", lambda x: self.app.delete_item()]],
    #     )
    #     detail_layout.add_widget(detail_toolbar)

    #     txt_field1 = MDTextField(
    #         text=element.get("name"), halign="left", hint_text="LIBELLE"
    #     )
    #     detail_layout.add_widget(txt_field1)

    #     txt_field2 = MDTextField(
    #         text=element.get("barcode"), halign="left", hint_text="BARCODE"
    #     )
    #     detail_layout.add_widget(txt_field2)

    #     detail_label1 = MDLabel(text=element.get("name"), halign="center")
    #     detail_layout.add_widget(detail_label1)

    #     detail_label2 = MDLabel(text=element.get("barcode"), halign="center")
    #     detail_layout.add_widget(detail_label2)

    #     slider = Slider(step=10, value=50)
    #     detail_layout.add_widget(slider)

    #     float_layout = FloatLayout(size_hint_y=None, height=dp(60))

    #     button_validation = MDRoundFlatIconButton(
    #         text="Valider",
    #         id="btn_save",
    #         icon="check",
    #         size_hint=(None, None),
    #         size=(150, 50),
    #         pos_hint={"center_x": 0.5},
    #         md_bg_color=[0.1, 0.5, 0.8, 1],  # Background color
    #         text_color=[1, 1, 1, 1],  # Text color
    #         line_color=[0.1, 0.5, 0.8, 1],  # Line color
    #     )
    #     float_layout.add_widget(button_validation)
    #     cm_to_pixels = dp(2 * 37.7952755906)  # 1 cm ≈ 37.7952755906 dp
    #     # Ajustement de la position après l'ajout au layout
    #     button_validation.bind(size=self.adjust_button_position)
    #     self.button = button_validation
    #     self.cm_to_pixels = cm_to_pixels
    #     button_validation.bind(size=self.adjust_button_position)

    #     button_validation2 = MDRoundFlatIconButton(
    #         text="Reset",
    #         id="btn_save",
    #         icon="check",
    #         size_hint=(None, None),
    #         size=(150, 50),
    #         pos_hint={"center_x": 0.5},
    #         md_bg_color=[0.1, 0.5, 0.8, 1],  # Background color
    #         text_color=[1, 1, 1, 1],  # Text color
    #         line_color=[0.1, 0.5, 0.8, 1],  # Line color
    #     )
    #     float_layout.add_widget(button_validation2)
    #     cm_to_pixels = dp(4 * 37.7952755906)  # 1 cm ≈ 37.7952755906 dp
    #     # Ajustement de la position après l'ajout au layout
    #     button_validation2.bind(size=self.adjust_button_position)
    #     self.button = button_validation2
    #     self.cm_to_pixels = cm_to_pixels
    #     button_validation2.bind(size=self.adjust_button_position)

    #     detail_layout.add_widget(float_layout)

    #     self.clear_widgets()
    #     self.add_widget(detail_layout)

    # def adjust_button_position(self, instance, value):
    #     self.button.y = self.cm_to_pixels
