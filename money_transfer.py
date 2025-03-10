import mysql.connector
import customtkinter as ctk
from tkinter import messagebox

class MoneyTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Transfer")
        self.root.geometry("400x500")  # Set window size
        self.root.attributes('-topmost', True)  # Keep window always on top

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        # GUI Components
        self.label = ctk.CTkLabel(root, text="Enter Your Account Number:")
        self.label.pack(pady=10)

        self.account_entry = ctk.CTkEntry(root)
        self.account_entry.pack(pady=5)

        self.submit_button = ctk.CTkButton(root, text="Proceed", command=self.verify_account)
        self.submit_button.pack(pady=10)

    def verify_account(self):
        account_number = self.account_entry.get()

        # Check if account exists
        self.cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        result = self.cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Account Verified! Proceeding with Payment.")
            self.root.destroy()  # Close verification window
            self.open_payment_window()
        else:
            messagebox.showerror("Error", "Invalid Account Number. Please Try Again.")

    def open_payment_window(self):
        # Open a new payment window
        payment_window = ctk.CTk()
        payment_window.title("Payment")
        payment_window.geometry("400x500")  # Set window size
        payment_window.attributes('-topmost', True)  # Keep window always on top

        label = ctk.CTkLabel(payment_window, text="Enter Amount to Transfer:")
        label.pack(pady=10)

        amount_entry = ctk.CTkEntry(payment_window)
        amount_entry.pack(pady=5)

        submit_button = ctk.CTkButton(payment_window, text="Pay", 
                                      command=lambda: self.process_payment(amount_entry.get(), payment_window))
        submit_button.pack(pady=10)

        payment_window.mainloop()

    def process_payment(self, amount, window):
        try:
            amount = float(amount)
            if amount > 0:
                messagebox.showinfo("Success", f"Payment of ₹{amount} successful!")
                window.destroy()  # Close payment window after success
            else:
                messagebox.showerror("Error", "Invalid Amount!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric amount.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MoneyTransferApp(root)
    root.mainloop()
