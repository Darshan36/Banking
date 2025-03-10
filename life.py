import customtkinter as ctk
import mysql.connector
import sys
from tkinter import messagebox, Toplevel

class LifeInsuranceApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Life Insurance")

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",  # Change this to your MySQL password
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        ctk.CTkLabel(self.root, text="Choose a Life Insurance Plan:", font=("Arial", 16)).pack(pady=10)

        # Available life insurance plans and descriptions
        self.insurance_plans = {
            "Term Insurance": (5000, "Provides coverage for a fixed term, offering a payout if the insured passes away during this period."),
            "Whole Life Insurance": (15000, "Covers the insured for their entire lifetime with a guaranteed payout upon death."),
            "Endowment Plan": (20000, "Combines life coverage with savings, offering a payout upon maturity or death."),
            "ULIP": (30000, "A Unit-Linked Insurance Plan that provides both investment growth and life coverage.")
        }

        # Create buttons for each insurance plan
        for plan, (cost, description) in self.insurance_plans.items():
            frame = ctk.CTkFrame(self.root)
            frame.pack(pady=5, padx=10, fill="x")

            # Button to purchase
            ctk.CTkButton(frame, text=f"{plan} - ₹{cost}", width=200, 
                          command=lambda p=plan, c=cost: self.purchase_insurance(p, c)).pack(side="left", padx=5)

            # Button for description
            ctk.CTkButton(frame, text="What does this mean?", width=150, fg_color="gray", 
                          command=lambda d=description: self.show_description(d)).pack(side="right", padx=5)

        # Frame to show previous insurances
        self.insurance_list_frame = ctk.CTkFrame(self.root)
        self.insurance_list_frame.pack(pady=10)
        self.show_previous_insurances()

    def show_previous_insurances(self):
        """Fetch and display previous life insurance plans dynamically."""
        for widget in self.insurance_list_frame.winfo_children():
            widget.destroy()  # Clear the frame before updating
        
        ctk.CTkLabel(self.insurance_list_frame, text="Your Purchased Life Insurance:", font=("Arial", 14)).pack(pady=5)

        self.cursor.execute("SELECT plan_name, cost FROM life_insurance WHERE account_number = %s", (self.account_number,))
        plans = self.cursor.fetchall()

        if plans:
            for plan, cost in plans:
                ctk.CTkLabel(self.insurance_list_frame, text=f"{plan} - ₹{cost}", font=("Arial", 12)).pack(pady=2)
        else:
            ctk.CTkLabel(self.insurance_list_frame, text="No life insurance purchased.", font=("Arial", 12)).pack(pady=2)

    def purchase_insurance(self, plan, cost):
        """Save selected life insurance plan to the database."""
        try:
            self.cursor.execute(
                "INSERT INTO life_insurance (account_number, plan_name, cost) VALUES (%s, %s, %s)",
                (self.account_number, plan, cost)
            )
            self.conn.commit()
            messagebox.showinfo("Success", f"You have purchased {plan} for ₹{cost}!")
            self.show_previous_insurances()  # Refresh list after purchasing

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def show_description(self, description):
        """Show a popup window with the insurance description."""
        desc_window = Toplevel(self.root)
        desc_window.title("Insurance Details")
        desc_window.geometry("400x200")
        ctk.CTkLabel(desc_window, text=description, wraplength=380, font=("Arial", 12),text_color="white",bg_color="darkblue").pack(pady=20, padx=20)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]
        root = ctk.CTk()
        app = LifeInsuranceApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
