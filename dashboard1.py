from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager

# Set window size (optional)
Window.size = (800, 600)

# Define the main dashboard layout
class DashboardLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10

        # Navigation Bar
        self.nav_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.nav_buttons = ["Home", "Pay", "Save", "Invest", "Borrow", "Insure", "Offers"]
        for button_text in self.nav_buttons:
            btn = Button(text=button_text, background_color=(0.2, 0.6, 1, 1))
            btn.bind(on_press=self.switch_content)
            self.nav_bar.add_widget(btn)
        self.add_widget(self.nav_bar)

        # Main Content Area
        self.content_area = BoxLayout(size_hint=(1, 0.8), orientation="vertical")
        self.add_widget(self.content_area)

        # Logout Button
        self.logout_button = Button(text="Logout", size_hint=(1, 0.1), background_color=(1, 0, 0, 1))
        self.logout_button.bind(on_press=self.logout)
        self.add_widget(self.logout_button)

        # Default content
        self.show_home_content()

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
        # Display home content
        self.content_area.add_widget(Label(text="Welcome to Your Banking Dashboard", font_size=24))

    def show_pay_content(self):
        # Display pay content
        self.content_area.add_widget(Label(text="Pay: Transfer Money, Pay Bills, Recharge", font_size=24))

    def show_save_content(self):
        # Display save content
        self.content_area.add_widget(Label(text="Save: Manage Savings Accounts", font_size=24))

    def show_invest_content(self):
        # Display invest content
        self.content_area.add_widget(Label(text="Invest: Explore Investment Options", font_size=24))

    def show_borrow_content(self):
        # Display borrow content
        self.content_area.add_widget(Label(text="Borrow: Apply for Loans", font_size=24))

    def show_insure_content(self):
        # Display insure content
        self.content_area.add_widget(Label(text="Insure: Get Insurance Plans", font_size=24))

    def show_offers_content(self):
        # Display offers content
        self.content_area.add_widget(Label(text="Offers: Check Out Latest Offers", font_size=24))

    def logout(self, instance):
        # Logout functionality
        print("Logged out successfully!")
        App.get_running_app().stop()

# Main App
class BankingApp(App):
    def build(self):
        return DashboardLayout()

# Run the app
if __name__ == "__main__":
    BankingApp().run()
