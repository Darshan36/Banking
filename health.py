import customtkinter as ctk
import mysql.connector
import sys
from tkinter import messagebox, Toplevel

class HealthInsuranceApp:
    def __init__(self, root, account_number):
        self.root = root
        self.account_number = account_number
        self.root.title("Health Insurance")

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",  # Change this to your MySQL password
            database="banking_system"
        )
        self.cursor = self.conn.cursor()

        # Family member selection
        ctk.CTkLabel(self.root, text="Select Family Member for Insurance:", font=("Arial", 14)).pack(pady=5)
        self.relations = ["Son", "Daughter", "Wife", "Husband", "Grandfather", "Grandmother"]
        self.selected_relation = ctk.StringVar(value=self.relations[0])

        dropdown = ctk.CTkOptionMenu(self.root, variable=self.selected_relation, values=self.relations)
        dropdown.pack(pady=5)

        # Age Entry
        ctk.CTkLabel(self.root, text="Enter Age:", font=("Arial", 12)).pack(pady=5)
        self.age_entry = ctk.CTkEntry(self.root)
        self.age_entry.pack(pady=5)

        # Sum Insured Selection
        self.insurance_plans = {
            50000: [1995, 2495, 3824, 4780, 7170, 8963],
            100000: [2993, 3742, 5736, 7170, 10755, 13444],
            150000: [3741, 4677, 7170, 8963, 13444, 16805],
            200000: [4676, 5846, 8963, 11203, 16805, 21006],
            300000: [5845, 7308, 11203, 14004, 21006, 26257],
            400000: [8767, 10962, 16805, 18905, 24919, 30248],
            500000: [10959, 13155, 21006, 23632, 29039, 36298]
        }

        ctk.CTkLabel(self.root, text="Select Sum Insured (SI):", font=("Arial", 12)).pack(pady=5)
        self.selected_si = ctk.IntVar(value=50000)
        dropdown_si = ctk.CTkOptionMenu(self.root, variable=self.selected_si, values=[str(si) for si in self.insurance_plans.keys()])
        dropdown_si.pack(pady=5)

        # Buttons
        self.purchase_btn = ctk.CTkButton(self.root, text="Purchase", command=self.calculate_premium)
        self.purchase_btn.pack(pady=5)

        self.info_btn = ctk.CTkButton(self.root, text="What does this mean?", command=self.show_details)
        self.info_btn.pack(pady=5)

        # Frame to show previous purchases
        self.insurance_list_frame = ctk.CTkFrame(self.root)
        self.insurance_list_frame.pack(pady=10)
        self.show_previous_insurances()

    def calculate_premium(self):
        """Calculate premium based on age and sum insured"""
        age_str = self.age_entry.get().strip()
        if not age_str.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid age.")
            return

        age = int(age_str)
        relation = self.selected_relation.get()
        si = self.selected_si.get()

        if age < 45:
            premium = int(si * 0.03)
        elif age >= 71:
            premium = self.insurance_plans[si][5]
        elif age >= 66:
            premium = self.insurance_plans[si][4]
        elif age >= 61:
            premium = self.insurance_plans[si][3]
        elif age >= 56:
            premium = self.insurance_plans[si][2]
        elif age >= 51:
            premium = self.insurance_plans[si][1]
        else:
            premium = self.insurance_plans[si][0]

        # Save in database
        try:
            self.cursor.execute(
                "INSERT INTO health_insurance (account_number, relation, age, sum_insured, premium) VALUES (%s, %s, %s, %s, %s)",
                (self.account_number, relation, age, si, premium)
            )
            self.conn.commit()
            messagebox.showinfo("Success", f"Purchased health insurance for {relation} (₹{premium})!")
            self.show_previous_insurances()  # Refresh list

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def show_previous_insurances(self):
        """Fetch and display previous health insurance plans"""
        for widget in self.insurance_list_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.insurance_list_frame, text="Your Health Insurance Plans:", font=("Arial", 14)).pack(pady=5)

        self.cursor.execute("SELECT relation, age, sum_insured, premium FROM health_insurance WHERE account_number = %s", (self.account_number,))
        plans = self.cursor.fetchall()

        if plans:
            for relation, age, si, premium in plans:
                ctk.CTkLabel(self.insurance_list_frame, text=f"{relation} ({age} yrs) - ₹{si} | Premium: ₹{premium}", font=("Arial", 12)).pack(pady=2)
        else:
            ctk.CTkLabel(self.insurance_list_frame, text="No health insurance purchased.", font=("Arial", 12)).pack(pady=2)

    def show_details(self):
        """Show a popup window with health insurance details"""
        desc_window = Toplevel(self.root)
        desc_window.title("Health Insurance Details")
        desc_window.geometry("400x250")
        desc_window.configure(bg="darkblue")
        description = (
            "Health insurance covers medical expenses for hospitalization, treatments, and more. \n\n"
            "Premiums are based on age and sum insured. \n"
            "- Below 45 years: 3% of total amount \n"
            "- Age 46+ follows predefined premiums. \n\n"
            "Ensure your family's well-being with the right plan."
        )
        ctk.CTkLabel(desc_window, text=description, wraplength=380, font=("Arial", 12),text_color="white",bg_color="darkblue").pack(pady=20, padx=20)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        account_number = sys.argv[1]
        root = ctk.CTk()
        app = HealthInsuranceApp(root, account_number)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Account number not provided!")
