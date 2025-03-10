import customtkinter as ctk
import mysql.connector
import sys
from tkinter import messagebox

class LockerApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Locker Management")

        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",  # Replace with your MySQL password
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        ctk.CTkLabel(self.root, text="Locker Registration", font=("Arial", 16)).pack(pady=10)

        # Show existing lockers
        self.show_existing_lockers()

        # PIN Entry
        ctk.CTkLabel(self.root, text="Enter 6-Digit PIN:", font=("Arial", 12)).pack(pady=5)
        self.pin_var = ctk.StringVar()
        self.pin_entry = ctk.CTkEntry(self.root, textvariable=self.pin_var, show="*", width=200)
        self.pin_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Confirm PIN:", font=("Arial", 12)).pack(pady=5)
        self.confirm_pin_var = ctk.StringVar()
        self.confirm_pin_entry = ctk.CTkEntry(self.root, textvariable=self.confirm_pin_var, show="*", width=200)
        self.confirm_pin_entry.pack(pady=5)

        self.register_btn = ctk.CTkButton(self.root, text="Register Locker", command=self.register_locker)
        self.register_btn.pack(pady=10)

    def show_existing_lockers(self):
        """Fetch and display the existing lockers for the user."""
        self.cursor.execute("SELECT locker_id FROM lockers WHERE account_number = %s", (self.account_number,))
        lockers = self.cursor.fetchall()

        if lockers:
            ctk.CTkLabel(self.root, text="Your Existing Lockers:", font=("Arial", 14)).pack(pady=5)
            for locker in lockers:
                ctk.CTkLabel(self.root, text=f"Locker ID: {locker[0]}", font=("Arial", 12)).pack()

    def register_locker(self):
        """Registers a new locker after PIN validation."""
        pin = self.pin_var.get().strip()
        confirm_pin = self.confirm_pin_var.get().strip()

        if len(pin) != 6 or not pin.isdigit():
            messagebox.showerror("Invalid PIN", "PIN must be exactly 6 digits.")
            return

        if pin != confirm_pin:
            messagebox.showerror("PIN Mismatch", "The entered PINs do not match.")
            return

        try:
            self.cursor.execute("INSERT INTO lockers (account_number, pin) VALUES (%s, %s)", 
                                (self.account_number, pin))
            self.conn.commit()
            messagebox.showinfo("Success", "Locker Registered Successfully!")

            self.pin_var.set("")
            self.confirm_pin_var.set("")
            self.root.destroy()  # Close the window after successful registration

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]
        root = ctk.CTk()
        app = LockerApp(root, account_number)
        root.mainloop()
    else:
        print("Error: Account number not provided!")
