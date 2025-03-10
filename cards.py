import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
import random
import sys



class CardsApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number  # Store the account number
        self.root.title("Your Cards")

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        self.display_cards()

    def display_cards(self):
        self.cursor.execute("SELECT card_number, card_type FROM cards WHERE account_number = %s", (self.account_number,))
        cards = self.cursor.fetchall()

        for widget in self.root.winfo_children():
            widget.destroy()  # Clear the window before updating

        if cards:
            for card_number, card_type in cards:
                ctk.CTkLabel(self.root, text=f"{card_type} Card: {card_number}").pack(pady=5)
        else:
            ctk.CTkLabel(self.root, text="No cards issued yet").pack(pady=5)

        # 🔹 Add the "Create Card" button
        create_button = ctk.CTkButton(self.root, text="Create Card", command=self.create_card)
        create_button.pack(pady=10)
    def create_card(self):
        """Opens a new window to create a debit or credit card."""
        self.new_window = ctk.CTkToplevel(self.root)
        self.new_window.geometry("300x200")
        self.new_window.title("Issue New Card")
        self.new_window.attributes('-topmost', True)

        label = ctk.CTkLabel(self.new_window, text="Select Card Type:", font=("Arial", 14))
        label.pack(pady=10)

        self.card_type_var = ctk.StringVar(value="Debit")

        debit_button = ctk.CTkRadioButton(self.new_window, text="Debit Card", variable=self.card_type_var, value="Debit")
        debit_button.pack()
        credit_button = ctk.CTkRadioButton(self.new_window, text="Credit Card", variable=self.card_type_var, value="Credit")
        credit_button.pack()

        submit_button = ctk.CTkButton(self.new_window, text="Issue Card", command=self.issue_card)
        submit_button.pack(pady=10)

    def issue_card(self):
        """Generates card details and stores them in the database."""
        card_type = self.card_type_var.get()
        card_number = self.generate_card_number()
        cvv = self.generate_cvv()

        try:
            self.cursor.execute("INSERT INTO cards (account_number, card_number, card_type, cvv) VALUES (%s, %s, %s, %s)", 
                            (self.account_number, card_number, card_type, cvv))
            self.conn.commit()
            messagebox.showinfo("Success", f"{card_type} Card Issued!\nCard Number: {card_number}\nCVV: {cvv}")
            self.new_window.destroy()
            self.display_cards()  # ✅ Corrected function call
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    @staticmethod
    def generate_card_number():
        """Generates a random 16-digit card number in XXXX XXXX XXXX XXXX format."""
        return ' '.join([''.join(str(random.randint(0, 9)) for _ in range(4)) for _ in range(4)])

    @staticmethod
    def generate_cvv():
        """Generates a random 3-digit CVV number."""
        return str(random.randint(100, 999))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]  # Get account number from command-line argument
        root = ctk.CTk()
        app = CardsApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
