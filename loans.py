import customtkinter as ctk
import mysql.connector
import sys
from tkinter import messagebox

class LoansApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Loan Application")

        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",  # Change to your MySQL password
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        # Loan types
        self.loans = {
            "Home Loan": "7-9% interest | 10-30 years",
            "Car Loan": "8-12% interest | 1-7 years",
            "Personal Loan": "10-16% interest | 1-5 years",
            "Education Loan": "4-10% interest | 5-15 years",
            "Gold Loan": "7-12% interest | 1-5 years",
            "Business Loan": "8-14% interest | 3-10 years"
        }

        ctk.CTkLabel(self.root, text="Select a Loan Type:", font=("Arial", 16)).pack(pady=10)
        
        self.loan_var = ctk.StringVar(value="Home Loan")
        self.dropdown = ctk.CTkComboBox(self.root, values=list(self.loans.keys()), variable=self.loan_var)
        self.dropdown.pack(pady=5)

        ctk.CTkLabel(self.root, text="Enter Loan Amount (INR):", font=("Arial", 12)).pack(pady=5)
        self.amount_entry = ctk.CTkEntry(self.root, width=200)
        self.amount_entry.pack(pady=5)

        self.apply_btn = ctk.CTkButton(self.root, text="Apply for Loan", command=self.apply_loan)
        self.apply_btn.pack(pady=10)

        self.info_btn = ctk.CTkButton(self.root, text="What does this mean?", command=self.show_info)
        self.info_btn.pack(pady=5)

    def apply_loan(self):
        loan_type = self.loan_var.get()
        loan_amount = self.amount_entry.get()

        if not loan_amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid loan amount!")
            return

        try:
            self.cursor.execute(
                "INSERT INTO loans (account_number, loan_type, loan_amount) VALUES (%s, %s, %s)",
                (self.account_number, loan_type, loan_amount)
            )
            self.conn.commit()
            messagebox.showinfo("Success", f"Loan for {loan_type} applied successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def show_info(self):
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Loan Details")
        info_window.configure(bg="darkblue")

        ctk.CTkLabel(
            info_window, 
            text="Loan Type Details:", 
            font=("Arial", 14),
            text_color="white",
            bg_color="darkblue"
        ).pack(pady=10)

        for loan, details in self.loans.items():
            ctk.CTkLabel(info_window, text=f"{loan}: {details}", font=("Arial", 12), text_color="white", bg_color="darkblue").pack(pady=2)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]
        root = ctk.CTk()
        app = LoansApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
