import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
import sys

class DepositApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Deposit Money")
        self.root.geometry("300x200")

        # Connect to database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        ctk.CTkLabel(self.root, text="Enter Amount:").pack(pady=10)
        self.amount_entry = ctk.CTkEntry(self.root)
        self.amount_entry.pack(pady=5)

        deposit_button = ctk.CTkButton(self.root, text="Deposit", command=self.deposit_money)
        deposit_button.pack(pady=10)

    def deposit_money(self):
        amount = self.amount_entry.get()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Enter a valid amount")
            return

        amount = float(amount)

        try:
            self.cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, self.account_number))
            self.conn.commit()
            messagebox.showinfo("Success", f"Deposited {amount} successfully!")
            self.root.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]
        root = ctk.CTk()
        app = DepositApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
