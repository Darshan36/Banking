import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
import sys

class BillPaymentsApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Bill Payments")
        self.root.geometry("400x500")
        self.root.attributes('-topmost', True)

        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        # Title Label
        ctk.CTkLabel(self.root, text="Select Bill Type", font=("Arial", 16)).pack(pady=10)

        # Bill Type Dropdown
        self.bill_types = ["Electricity", "Water", "Internet", "Gas", "Phone"]
        self.selected_bill = ctk.StringVar(value=self.bill_types[0])
        self.bill_dropdown = ctk.CTkOptionMenu(self.root, variable=self.selected_bill, values=self.bill_types)
        self.bill_dropdown.pack(pady=5)

        # Amount Entry
        ctk.CTkLabel(self.root, text="Enter Amount:", font=("Arial", 14)).pack(pady=10)
        self.amount_entry = ctk.CTkEntry(self.root)
        self.amount_entry.pack(pady=5)

        # Pay Button
        ctk.CTkButton(self.root, text="Pay Bill", command=self.pay_bill).pack(pady=10)

        # Display Previous Payments
        self.display_previous_payments()

    def pay_bill(self):
        bill_type = self.selected_bill.get()
        amount = self.amount_entry.get()

        # Validate Amount
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")
            return

        # Insert Payment into Database
        try:
            self.cursor.execute(
                "INSERT INTO bill_payments (account_number, bill_type, amount) VALUES (%s, %s, %s)",
                (self.account_number, bill_type, amount)
            )
            self.conn.commit()
            messagebox.showinfo("Success", f"Paid ₹{amount} for {bill_type} bill.")
            self.amount_entry.delete(0, 'end')
            self.display_previous_payments()  # Refresh payment history
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def display_previous_payments(self):
        # Remove old records from UI
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and "Paid" in widget.cget("text"):
                widget.destroy()

        # Fetch Last 5 Payments
        self.cursor.execute("SELECT bill_type, amount, payment_date FROM bill_payments WHERE account_number = %s ORDER BY payment_date DESC LIMIT 5", (self.account_number,))
        payments = self.cursor.fetchall()

        if payments:
            ctk.CTkLabel(self.root, text="Last 5 Payments:", font=("Arial", 14, "bold")).pack(pady=10)
            for bill_type, amount, date in payments:
                ctk.CTkLabel(self.root, text=f"Paid ₹{amount} for {bill_type} on {date}").pack(pady=2)
        else:
            ctk.CTkLabel(self.root, text="No previous payments found.").pack(pady=5)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]  # Get account number from command-line argument
        root = ctk.CTk()
        app = BillPaymentsApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
