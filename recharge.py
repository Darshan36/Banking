import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
import sys
import random

class RechargeApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Mobile Recharge")
        self.root.geometry("400x500")
        self.root.attributes('-topmost', True)

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        # Recharge Options
        ctk.CTkLabel(root, text="Enter Mobile Number:").pack(pady=5)
        self.mobile_entry = ctk.CTkEntry(root)
        self.mobile_entry.pack(pady=5)

        ctk.CTkLabel(root, text="Enter Amount:").pack(pady=5)
        self.amount_entry = ctk.CTkEntry(root)
        self.amount_entry.pack(pady=5)

        ctk.CTkLabel(root, text="Select Operator:").pack(pady=5)
        self.operator_var = ctk.StringVar(value="Airtel")
        operators = ["Airtel", "Jio", "Vi", "BSNL"]
        for op in operators:
            ctk.CTkRadioButton(root, text=op, variable=self.operator_var, value=op).pack()

        pay_button = ctk.CTkButton(root, text="Proceed to Recharge", command=self.process_recharge)
        pay_button.pack(pady=10)

    def process_recharge(self):
        mobile = self.mobile_entry.get()
        amount = self.amount_entry.get()
        operator = self.operator_var.get()

        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Error", "Enter a valid 10-digit mobile number.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Enter a valid amount.")
                return
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        transaction_id = self.generate_transaction_id()

        # Insert into recharge table
        try:
            self.cursor.execute("""
                INSERT INTO recharges (account_number, mobile_number, amount, operator, transaction_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (self.account_number, mobile, amount, operator, transaction_id))
            self.conn.commit()
            messagebox.showinfo("Success", f"Recharge Successful!\nTransaction ID: {transaction_id}")
            self.root.destroy()  # Close the window after success
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    @staticmethod
    def generate_transaction_id():
        """Generates a random 12-digit transaction ID."""
        return ''.join(str(random.randint(0, 9)) for _ in range(12))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]  # Get account number from command-line arguments
        root = ctk.CTk()
        app = RechargeApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
