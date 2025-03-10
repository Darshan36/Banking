from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

# Set window size (optional)
Window.size = (800, 600)

# Screen Manager
class BankingApp(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.screen_manager.add_widget(LoginScreen(name="login"))
        self.screen_manager.add_widget(DashboardScreen(name="dashboard"))
        return self.screen_manager

# Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=50, spacing=20)

        # Background Image
        self.bg = Image(source="Welcome.png", allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)

        # Login Form
        self.form = BoxLayout(orientation="vertical", size_hint=(0.8, None), spacing=10)
        self.form.bind(minimum_height=self.form.setter('height'))

        self.username = TextInput(hint_text="Username", size_hint=(1, None), height=50)
        self.password = TextInput(hint_text="Password", password=True, size_hint=(1, None), height=50)
        self.mpin = TextInput(hint_text="MPIN (4-digit)", password=True, size_hint=(1, None), height=50)
        self.otp = TextInput(hint_text="Enter OTP", size_hint=(1, None), height=50)

        self.form.add_widget(self.username)
        self.form.add_widget(self.password)
        self.form.add_widget(self.mpin)
        self.form.add_widget(self.otp)

        self.login_button = Button(text="Login", size_hint=(1, None), height=50, background_color=(0, 0.7, 0, 1))
        self.login_button.bind(on_press=self.login)

        self.register_button = Button(text="Register", size_hint=(1, None), height=50, background_color=(0.2, 0.6, 1, 1))
        self.register_button.bind(on_press=self.register)

        self.form.add_widget(self.login_button)
        self.form.add_widget(self.register_button)

        self.layout.add_widget(self.form)
        self.add_widget(self.layout)

    def login(self, instance):
        # Simulate login success
        self.parent.current = "dashboard"

    def register(self, instance):
        # Show registration popup
        popup = Popup(title="Register", size_hint=(0.8, 0.6))
        popup.content = RegisterForm(popup)
        popup.open()

# Registration Form
class RegisterForm(BoxLayout):
    def __init__(self, popup, **kwargs):
        super().__init__(**kwargs)
        self.popup = popup
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        self.username = TextInput(hint_text="Username", size_hint=(1, None), height=50)
        self.password = TextInput(hint_text="Password", password=True, size_hint=(1, None), height=50)
        self.email = TextInput(hint_text="Email", size_hint=(1, None), height=50)
        self.mpin = TextInput(hint_text="MPIN (4-digit)", password=True, size_hint=(1, None), height=50)

        self.register_button = Button(text="Register", size_hint=(1, None), height=50, background_color=(0, 0.7, 0, 1))
        self.register_button.bind(on_press=self.register)

        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.email)
        self.add_widget(self.mpin)
        self.add_widget(self.register_button)

    def register(self, instance):
        # Simulate registration
        self.popup.dismiss()

# Dashboard Screen
class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        # Navigation Bar
        self.nav_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.nav_buttons = ["Home", "Pay", "Save", "Invest", "Borrow", "Insure", "Offers"]
        for button_text in self.nav_buttons:
            btn = Button(text=button_text, background_color=(0.2, 0.6, 1, 1))
            btn.bind(on_press=self.switch_content)
            self.nav_bar.add_widget(btn)
        self.layout.add_widget(self.nav_bar)

        # Content Area
        self.content_area = BoxLayout(size_hint=(1, 0.9), orientation="vertical")
        self.layout.add_widget(self.content_area)

        # Default content
        self.show_home_content()

        self.add_widget(self.layout)

    def switch_content(self, instance):
        # Switch content based on the button pressed
        button_text = instance.text
        self.content_area.clear_widgets()

        if button_text == "Home":
            self.show_home_content()
        elif button_text == "Pay":
            self.show_pay_content()
        elif button_text == "Save":
            self.show_save_content()
        elif button_text == "Invest":
            self.show_invest_content()
        elif button_text == "Borrow":
            self.show_borrow_content()
        elif button_text == "Insure":
            self.show_insure_content()
        elif button_text == "Offers":
            self.show_offers_content()

    def show_home_content(self):
        self.content_area.add_widget(Label(text="Welcome to Your Banking Dashboard", font_size=24))

    def show_pay_content(self):
        self.content_area.add_widget(Label(text="Pay: Transfer Money, Pay Bills, Recharge", font_size=24))

    def show_save_content(self):
        self.content_area.add_widget(Label(text="Save: Manage Savings Accounts", font_size=24))

    def show_invest_content(self):
        self.content_area.add_widget(Label(text="Invest: Explore Investment Options", font_size=24))

    def show_borrow_content(self):
        self.content_area.add_widget(Label(text="Borrow: Apply for Loans", font_size=24))

    def show_insure_content(self):
        self.content_area.add_widget(Label(text="Insure: Get Insurance Plans", font_size=24))

    def show_offers_content(self):
        self.content_area.add_widget(Label(text="Offers: Check Out Latest Offers", font_size=24))

# Run the app
if __name__ == "__main__":
    BankingApp().run()
