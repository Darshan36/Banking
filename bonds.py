import customtkinter as ctk
import webbrowser
import sys

class BondsApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Bond Investments")

        ctk.CTkLabel(self.root, text="Explore Bond Investment Platforms:", font=("Arial", 16)).pack(pady=10)

        # List of investment platforms
        self.investment_links = {
            "Jiraaf": "https://www.jiraaf.com/",
            "The Fixed Income": "https://www.thefixedincome.com/",
            "Investopedia": "https://www.investopedia.com/",
            "Grip Invest": "https://www.gripinvest.in/"
        }

        # Create buttons for each platform
        for name, link in self.investment_links.items():
            btn = ctk.CTkButton(self.root, text=name, command=lambda l=link: self.open_investment_site(l))
            btn.pack(pady=5)

    def open_investment_site(self, link):
        """Opens the selected investment site in the default browser."""
        webbrowser.open(link)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]
        root = ctk.CTk()
        app = BondsApp(root, account_number)
        root.mainloop()
    else:
        print("Error: Account number not provided!")
