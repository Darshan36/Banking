import customtkinter as ctk
import math

class EMI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("EMI Calculator")

        # Labels and Inputs
        ctk.CTkLabel(root, text="Loan Amount (₹):", font=("Arial", 14)).pack(pady=5)
        self.amount_entry = ctk.CTkEntry(root)
        self.amount_entry.pack(pady=5)

        ctk.CTkLabel(root, text="Annual Interest Rate (%):", font=("Arial", 14)).pack(pady=5)
        self.rate_entry = ctk.CTkEntry(root)
        self.rate_entry.pack(pady=5)

        ctk.CTkLabel(root, text="Loan Tenure (Years):", font=("Arial", 14)).pack(pady=5)
        self.tenure_entry = ctk.CTkEntry(root)
        self.tenure_entry.pack(pady=5)

        # Calculate Button
        self.calculate_btn = ctk.CTkButton(root, text="Calculate EMI", command=self.calculate_emi)
        self.calculate_btn.pack(pady=10)

        # Output Label
        self.result_label = ctk.CTkLabel(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

    def calculate_emi(self):
        try:
            principal = float(self.amount_entry.get())
            rate = float(self.rate_entry.get()) / (12 * 100)  # Convert annual rate to monthly
            tenure = int(self.tenure_entry.get()) * 12  # Convert years to months

            if rate == 0:  # If interest rate is 0%
                emi = principal / tenure
            else:
                emi = (principal * rate * (math.pow(1 + rate, tenure))) / (math.pow(1 + rate, tenure) - 1)

            self.result_label.configure(text=f"Monthly EMI: ₹{emi:.2f}")
        
        except ValueError:
            self.result_label.configure(text="Invalid Input! Please enter valid numbers.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = EMI_Calculator(root)
    root.mainloop()
