import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
import sys


class SavingsAccountApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Open Savings Account")

        # Connect to the existing banking_system database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        # Check if the user already has a savings account
        self.cursor.execute("SELECT has_savings_account FROM accounts WHERE account_number = %s", (self.account_number,))
        result = self.cursor.fetchone()

        if result and result[0]:  # If has_savings_account is True
            messagebox.showinfo("Info", "You already have a savings account.")
            self.root.destroy()
            return

        # UI Elements
        ctk.CTkLabel(self.root, text="Enter Initial Deposit:", font=("Arial", 14)).pack(pady=10)
        self.deposit_entry = ctk.CTkEntry(self.root)
        self.deposit_entry.pack(pady=5)

        submit_button = ctk.CTkButton(self.root, text="Create Savings Account", command=self.create_savings_account)
        submit_button.pack(pady=10)

    def create_savings_account(self):
        """Creates a new savings account for the logged-in user."""
        deposit_amount = self.deposit_entry.get()

        if not deposit_amount.isdigit() or int(deposit_amount) < 100:
            messagebox.showerror("Error", "Minimum deposit is ₹100")
            return

        try:
            self.cursor.execute(
                "INSERT INTO savings_accounts (account_number, balance) VALUES (%s, %s)",
                (self.account_number, deposit_amount)
            )
            self.cursor.execute("UPDATE accounts SET has_savings_account = TRUE WHERE account_number = %s",
                                (self.account_number,))
            self.conn.commit()
            messagebox.showinfo("Success", "Savings Account Created Successfully!")
            self.root.destroy()  # Close window after creation
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]  # Get account number from command-line argument
        root = ctk.CTk()
        app = SavingsAccountApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
