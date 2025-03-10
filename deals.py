import customtkinter as ctk
import random
import string
import pyperclip

class DealsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recent Deals")

        ctk.CTkLabel(root, text="🔥 Recent Deals 🔥", font=("Arial", 18, "bold")).pack(pady=10)

        self.deals = [
            "50% Off on Car Insurance",
            "20% Discount on Health Insurance",
            "0% EMI on Home Loans",
            "Buy 1 Get 1 Free - Life Insurance"
        ]

        self.coupon_labels = {}  # Store coupon labels
        self.copy_buttons = {}  # Store copy buttons

        for deal in self.deals:
            btn = ctk.CTkButton(root, text=deal, command=lambda d=deal: self.show_coupon(d))
            btn.pack(pady=5)

            # Label for the generated coupon (initially hidden)
            coupon_label = ctk.CTkLabel(root, text="", font=("Arial", 14), fg_color="gray20", width=200)
            coupon_label.pack(pady=2)
            self.coupon_labels[deal] = coupon_label

            # Copy button (initially hidden)
            copy_btn = ctk.CTkButton(root, text="Copy", command=lambda d=deal: self.copy_to_clipboard(d), fg_color="blue", text_color="white")
            copy_btn.pack(pady=2)
            copy_btn.pack_forget()  # Hide initially
            self.copy_buttons[deal] = copy_btn

    def generate_coupon(self, length=8):
        """Generates a random coupon code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def show_coupon(self, deal):
        """Displays the coupon code below the clicked deal."""
        coupon = self.generate_coupon()
        self.coupon_labels[deal].configure(text=f"Coupon Code: {coupon}")
        self.coupon_labels[deal].pack()
        self.copy_buttons[deal].pack()  # Show copy button
        self.copy_buttons[deal].coupon = coupon  # Store the coupon

    def copy_to_clipboard(self, deal):
        """Copies the coupon code to clipboard."""
        coupon = self.copy_buttons[deal].coupon
        pyperclip.copy(coupon)
        self.copy_buttons[deal].configure(text="Copied!", fg_color="green")
        self.root.after(1000, lambda: self.copy_buttons[deal].configure(text="Copy", fg_color="blue"))

if __name__ == "__main__":
    root = ctk.CTk()
    app = DealsApp(root)
    root.mainloop()
