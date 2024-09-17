import random
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp


class RegistrationScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class ProfileScreen(Screen):
    def on_enter(self):
        username = self.manager.get_screen('menu').ids.name.text.split(", ")[1]
        self.ids.profile_label.text = f"User: {username}\nUniversity: BMSTU\nAge: 19\nFavourite unit: Knight"


class AboutUsScreen(Screen):
    pass


class BattlesScreen(Screen):
    pass


class CalculatorScreen(Screen):
    pass


class MainApp(MDApp):
    dropdown = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        return Builder.load_file('Main_new.kv')

    def switch_to_menu(self):
        username = self.root.get_screen('registration').ids.user.text
        self.root.get_screen('menu').ids.name.text = f"Welcome back, {username}"
        self.root.current = 'menu'

    def reset_fields(self):
        self.root.get_screen('registration').ids.welcome_label.text = "Welcome to Bauman's Gate"
        self.root.get_screen('registration').ids.user.text = ""
        self.root.get_screen('registration').ids.password.text = ""

    def open_dropdown(self, widget):
        dropdown = DropDown()
        for unit in ["Мечник", "Топорщик", "Копьеносец", "Лучник с дл. луком", "Лучник с кор. луком", "Арбалетчик",
                     "Рыцарь", "Конный лучник", "Кирасир"]:
            btn = Button(text=unit, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        dropdown.open(widget)
        dropdown.bind(on_select=lambda instance, x: setattr(widget, 'text', x))

    def get_points(self, lst_of_units):
        points = 0
        for unit in lst_of_units:
            if unit == "Мечник":
                points += 58
            elif unit == "Топорщик":
                points += 48
            elif unit == "Копьеносец":
                points += 39
            elif unit == "Лучник с дл. луком":
                points += 38
            elif unit == "Лучник с кор. луком":
                points += 29
            elif unit == "Арбалетчик":
                points += 43
            elif unit == "Рыцарь":
                points += 33
            elif unit == "Конный лучник":
                points += 27
            elif unit == "Кирасир":
                points += 57
        return points

    def calculate_cost(self):
        lst_of_units = ["Мечник", "Топорщик", "Копьеносец", "Лучник с дл. луком", "Лучник с кор. луком", "Арбалетчик",
                        "Рыцарь", "Конный лучник", "Кирасир"]
        unit1 = self.root.get_screen('calculator').ids.unit1.text
        unit2 = self.root.get_screen('calculator').ids.unit2.text
        unit3 = self.root.get_screen('calculator').ids.unit3.text
        unit4 = self.root.get_screen('calculator').ids.unit4.text
        bot_unit1 = random.choice(lst_of_units)
        bot_unit2 = random.choice(lst_of_units)
        bot_unit3 = random.choice(lst_of_units)
        bot_unit4 = random.choice(lst_of_units)
        lst_of_bots = ["Кирасир", "Кирасир", "Кирасир", "Кирасир"]
        # lst_of_bots = [bot_unit1, bot_unit2, bot_unit3, bot_unit4]
        lst_of_users = [unit1, unit2, unit3, unit4]
        bot_points = self.get_points(lst_of_bots)
        user_points = self.get_points(lst_of_users)
        if user_points - bot_points >= 5:
            self.root.get_screen('menu').ids.name.text = f"Вы выиграли"
            self.root.current = 'menu'
        elif user_points - bot_points <= -5:
            self.root.get_screen('menu').ids.name.text = "Бот выиграл"
            self.root.current = 'menu'
        else:
            self.root.get_screen('menu').ids.name.text = "Исход не определен"
            self.root.current = 'menu'


if __name__ == '__main__':
    MainApp().run()
