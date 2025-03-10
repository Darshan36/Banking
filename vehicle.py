import customtkinter as ctk
import mysql.connector
import sys
import re
from tkinter import messagebox, Toplevel

class VehicleInsuranceApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Vehicle Insurance")

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",  # Change this to your MySQL password
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        # Frame to display previous registrations
        self.vehicle_list_frame = ctk.CTkFrame(self.root)
        self.vehicle_list_frame.pack(pady=5)

        ctk.CTkLabel(self.root, text="Enter Vehicle Registration Number:", font=("Arial", 16)).pack(pady=10)

        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self.root, textvariable=self.entry_var, width=200)
        self.entry.pack(pady=5)

        self.submit_btn = ctk.CTkButton(self.root, text="Submit", command=self.validate_and_submit)
        self.submit_btn.pack(pady=10)

        # Load previous vehicles
        self.show_previous_insurances()

    def show_previous_insurances(self):
        """Fetch and display previous vehicle registrations (refreshable)."""
        for widget in self.vehicle_list_frame.winfo_children():
            widget.destroy()  # Clear the frame before updating
        
        ctk.CTkLabel(self.vehicle_list_frame, text="Your Registered Vehicles:", font=("Arial", 14)).pack(pady=5)

        self.cursor.execute("SELECT vehicle_number, model FROM vehicle_insurance WHERE account_number = %s", (self.account_number,))
        vehicles = self.cursor.fetchall()

        if vehicles:
            for v_number, model in vehicles:
                ctk.CTkLabel(self.vehicle_list_frame, text=f"{v_number} - {model}", font=("Arial", 12)).pack(pady=2)
        else:
            ctk.CTkLabel(self.vehicle_list_frame, text="No vehicles registered.", font=("Arial", 12)).pack(pady=2)

    def validate_and_submit(self):
        vehicle_number = self.entry_var.get().strip().upper()
        pattern = r'^[A-Z]{2}\s\d{2}\s[A-Z]{2}\s[A-Z0-9]{4}$'  # Format: MH 12 AB 1234

        if not re.match(pattern, vehicle_number):
            messagebox.showerror("Invalid Format", "Enter in format: 'MH 12 AB 1234'")
            return

        try:
            # Insert into database
            self.cursor.execute(
                "INSERT INTO vehicle_insurance (account_number, vehicle_number, model, insurance_cost) VALUES (%s, %s, %s, %s)",
                (self.account_number, vehicle_number, "Not Selected", 0.00)
            )
            self.conn.commit()

            messagebox.showinfo("Success", f"Vehicle '{vehicle_number}' Registered Successfully!")

            self.show_previous_insurances()  # **Refresh vehicle list immediately**
            self.entry_var.set("")  # Clear input field
            self.open_insurance_selection(vehicle_number)  # Open insurance selection window

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def open_insurance_selection(self, vehicle_number):
        """Open insurance selection window after registering a vehicle."""
        insurance_window = Toplevel(self.root)
        insurance_window.title("Select Insurance Plan")

        ctk.CTkLabel(insurance_window, text="Choose Vehicle Type:", font=("Arial", 16)).pack(pady=10)

        ctk.CTkButton(insurance_window, text="4-Wheelers", command=lambda: self.select_four_wheeler(vehicle_number, insurance_window)).pack(pady=5)
        ctk.CTkButton(insurance_window, text="2-Wheelers", command=lambda: self.select_two_wheeler(vehicle_number, insurance_window)).pack(pady=5)

    def select_four_wheeler(self, vehicle_number, window):
        """Show four-wheeler options and update insurance cost."""
        window.destroy()
        options = {
            "Hatchback": 15000,
            "Sedan": 20000,
            "SUV": 25000,
            "Luxury Car": 60000
        }
        self.show_insurance_options(vehicle_number, options, "4-Wheeler")

    def select_two_wheeler(self, vehicle_number, window):
        """Show two-wheeler options and update insurance cost."""
        window.destroy()
        options = {
            "Less than 75cc": 2901,
            "75cc to 150cc": 3851,
            "150cc to 350cc": 7365,
            "More than 350cc": 15117
        }
        self.show_insurance_options(vehicle_number, options, "2-Wheeler")

    def show_insurance_options(self, vehicle_number, options, vehicle_type):
        """Display insurance options and update database on selection."""
        selection_window = Toplevel(self.root)
        selection_window.title(f"Select {vehicle_type} Model")

        ctk.CTkLabel(selection_window, text="Choose Model:", font=("Arial", 16)).pack(pady=10)

        for model, cost in options.items():
            ctk.CTkButton(selection_window, text=f"{model} - ₹{cost}", 
                          command=lambda m=model, c=cost: self.finalize_insurance(vehicle_number, m, c, selection_window)).pack(pady=5)

    def finalize_insurance(self, vehicle_number, model, cost, window):
        """Update the database with the selected insurance plan."""
        try:
            self.cursor.execute(
                "UPDATE vehicle_insurance SET model = %s, insurance_cost = %s WHERE vehicle_number = %s",
                (model, cost, vehicle_number)
            )
            self.conn.commit()
            messagebox.showinfo("Success", f"Insurance for {model} registered at ₹{cost}!")
            window.destroy()  # Close the selection window
            self.show_previous_insurances()  # **Refresh list after insurance selection**

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]
        root = ctk.CTk()
        app = VehicleInsuranceApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
