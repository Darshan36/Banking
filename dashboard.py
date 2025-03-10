import customtkinter as ctk
from tkinter import messagebox
from itertools import cycle
from PIL import Image, ImageTk
import mysql.connector
import sys
import subprocess
from tkcalendar import Calendar
import random


# Check if the account number is provided when opening the dashboard
if len(sys.argv) > 1:
    logged_in_account_number = sys.argv[1]  # Get account number from command-line arguments
else:
    messagebox.showerror("Error", "Account number not provided!")
    sys.exit(1)  # Exit if account number is missing

# Example: When opening `cards.py`, pass the account number
def open_cards():
    subprocess.run(["python", "cards.py", logged_in_account_number])


class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Dashboard")
        self.root.geometry("1920x1080")  # Fullscreen size
        self.username = username
        self.welcome_label = ctk.CTkLabel(root, text=f"Welcome, {self.username}",
                                  font=("Arial", 18, "bold"), fg_color="#1F3A68")
        self.welcome_label.pack(pady=(10, 5), fill="x")  # Ensure it spans the width
        self.images = ["image1.png", "image2.png", "image3.png"]  # Replace with actual image paths
        self.image_cycle = cycle(self.images)  # Create a cycle iterator for the images

        self.nav_frame = ctk.CTkFrame(root, fg_color="#1F3A68")
        self.nav_frame.pack(fill="x", pady=(0, 10))  # Add padding below the navigation bar
        # Database Connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="FWbdT#R2",
            database="banking_system"
        )
        self.cursor = self.db.cursor()

        
        
        # User Login (Hardcoded for now, can be dynamic later)
        self.account_id = 1
        self.cursor.execute("SELECT username, balance FROM accounts WHERE id=%s", (self.account_id,))
        result = self.cursor.fetchone()
        self.username, self.balance = result if result else ("Unknown", 0)
        
        
        
        self.create_nav_button("\U0001F3E0 HOME", 0)
        self.create_pay_button("\U0001F4B3 PAY", 1)  # Use create_pay_button for the PAY button
        self.create_save_button("\U0001F4BC SAVE", 2)
        self.create_invest_button("\U0001F4C8 INVEST", 3)
        self.create_borrow_button("\U0001F4B8 BORROW", 4)
        self.create_insure_button("\U0001F4E3 INSURE", 5)
        self.create_offers_button("\U0001F6D2 OFFERS", 6)

        self.logout_button = ctk.CTkButton(self.nav_frame, text="Logout", fg_color="red", hover_color="darkred", command=self.logout)
        self.logout_button.grid(row=0, column=7, padx=250, pady=5, sticky="e")

        
        
        # Slideshow
        self.slideshow_frame = ctk.CTkFrame(root)
        self.slideshow_frame.place(relx=0.5, rely=0.572, anchor="center")  # Add padding to separate from the navigation bar

        # Add the image label to the slideshow frame
        self.image_label = ctk.CTkLabel(self.slideshow_frame, text="")
        self.image_label.pack()

        # Add navigation buttons to the slideshow frame
        self.prev_button = ctk.CTkButton(self.slideshow_frame, text="<", command=self.prev_image, width=40, height=40, corner_radius=20, fg_color="gray", hover_color="darkgray")
        self.prev_button.pack(side="left", padx=10)  # Place on the left side

        self.next_button = ctk.CTkButton(self.slideshow_frame, text=">", command=self.next_image, width=40, height=40, corner_radius=20, fg_color="gray", hover_color="darkgray")
        self.next_button.pack(side="right", padx=10)
        self.update_slideshow()
        #self.current_image = None
        
        #self.slideshow_frame.pack(pady=20)

 
    
    def create_nav_button(self, text, column):
        button = ctk.CTkButton(self.nav_frame, text=text, fg_color="#1F3A68", hover_color="#14284D")
        button.grid(row=0, column=column, padx=10, pady=5)

    

    def create_pay_button(self, text, column):
        self.pay_button = ctk.CTkButton(self.nav_frame, text=text, fg_color="#1F3A68", hover_color="#14284D")
        self.pay_button.grid(row=0, column=column, padx=10, pady=5)
    
        # Create Pay Menu Frame (Hidden initially)
        self.pay_menu = ctk.CTkFrame(self.root, fg_color="#1F3A68", corner_radius=5, width=200, height=120)  # Set width and height here
    
        options = ["Money Transfer", "Cards", "Bill Payments", "Recharge"]
        for i, option in enumerate(options):
            btn = ctk.CTkButton(self.pay_menu, text=option, fg_color="#1F3A68", hover_color="#14284D", 
                            command=lambda opt=option: self.pay_option_selected(opt))
            btn.pack(fill='x', pady=2)

        # Bind hover events
        self.pay_button.bind("<Enter>", self.show_pay_options)
        self.pay_menu.bind("<Enter>", self.cancel_hide_pay_options)
        self.pay_menu.bind("<Leave>", self.schedule_hide_pay_options)
        self.pay_button.bind("<Leave>", self.schedule_hide_pay_options)

    def create_save_button(self, text, column):
        self.save_button = ctk.CTkButton(self.nav_frame, text=text, fg_color="#1F3A68", hover_color="#14284D")
        self.save_button.grid(row=0, column=column, padx=10, pady=5)
    
        # Create Save Menu Frame (Hidden initially)
        self.save_menu = ctk.CTkFrame(self.root, fg_color="#1F3A68", corner_radius=5, width=200, height=120)  # Set width and height here
    
        options = ["Accounts", "Deposits", "Locker"]
        for i, option in enumerate(options):
            btn = ctk.CTkButton(self.save_menu, text=option, fg_color="#1F3A68", hover_color="#14284D", 
                            command=lambda opt=option: self.save_option_selected(opt))
            btn.pack(fill='x', pady=2)

        # Bind hover events
        self.save_button.bind("<Enter>", self.show_save_options)
        self.save_menu.bind("<Enter>", self.cancel_hide_save_options)
        self.save_menu.bind("<Leave>", self.schedule_hide_save_options)
        self.save_button.bind("<Leave>", self.schedule_hide_save_options)

    def create_invest_button(self, text, column):
        self.invest_button = ctk.CTkButton(self.nav_frame, text=text, fg_color="#1F3A68", hover_color="#14284D")
        self.invest_button.grid(row=0, column=column, padx=10, pady=5)
    
        # Create Invest Menu Frame (Hidden initially)
        self.invest_menu = ctk.CTkFrame(self.root, fg_color="#1F3A68", corner_radius=5, width=200, height=120)  # Set width and height here
    
        options = ["Bonds", "Mutual Funds"]
        for i, option in enumerate(options):
            btn = ctk.CTkButton(self.invest_menu, text=option, fg_color="#1F3A68", hover_color="#14284D", 
                            command=lambda opt=option: self.invest_option_selected(opt))
            btn.pack(fill='x', pady=2)

        # Bind hover events
        self.invest_button.bind("<Enter>", self.show_invest_options)
        self.invest_menu.bind("<Enter>", self.cancel_hide_invest_options)
        self.invest_menu.bind("<Leave>", self.schedule_hide_invest_options)
        self.invest_button.bind("<Leave>", self.schedule_hide_invest_options)

    def create_borrow_button(self, text, column):
        self.borrow_button = ctk.CTkButton(self.nav_frame, text=text, fg_color="#1F3A68", hover_color="#14284D")
        self.borrow_button.grid(row=0, column=column, padx=10, pady=5)
    
        # Create Borrow Menu Frame (Hidden initially)
        self.borrow_menu = ctk.CTkFrame(self.root, fg_color="#1F3A68", corner_radius=5, width=200, height=120)  # Set width and height here
    
        options = ["Loans", "EMI"]
        for i, option in enumerate(options):
            btn = ctk.CTkButton(self.borrow_menu, text=option, fg_color="#1F3A68", hover_color="#14284D", 
                            command=lambda opt=option: self.borrow_option_selected(opt))
            btn.pack(fill='x', pady=2)

        # Bind hover events
        self.borrow_button.bind("<Enter>", self.show_borrow_options)
        self.borrow_menu.bind("<Enter>", self.cancel_hide_borrow_options)
        self.borrow_menu.bind("<Leave>", self.schedule_hide_borrow_options)
        self.borrow_button.bind("<Leave>", self.schedule_hide_borrow_options)

    def create_insure_button(self, text, column):
        self.insure_button = ctk.CTkButton(self.nav_frame, text=text, fg_color="#1F3A68", hover_color="#14284D")
        self.insure_button.grid(row=0, column=column, padx=10, pady=5)
    
        # Create Insure Menu Frame (Hidden initially)
        self.insure_menu = ctk.CTkFrame(self.root, fg_color="#1F3A68", corner_radius=5, width=200, height=120)  # Set width and height here
    
        options = ["Life", "Vehicle", "Health"]
        for i, option in enumerate(options):
            btn = ctk.CTkButton(self.insure_menu, text=option, fg_color="#1F3A68", hover_color="#14284D", 
                            command=lambda opt=option: self.insure_option_selected(opt))
            btn.pack(fill='x', pady=2)

        # Bind hover events
        self.insure_button.bind("<Enter>", self.show_insure_options)
        self.insure_menu.bind("<Enter>", self.cancel_hide_insure_options)
        self.insure_menu.bind("<Leave>", self.schedule_hide_insure_options)
        self.insure_button.bind("<Leave>", self.schedule_hide_insure_options)

    def create_offers_button(self, text, column):
        self.offers_button = ctk.CTkButton(self.nav_frame, text=text, fg_color="#1F3A68", hover_color="#14284D")
        self.offers_button.grid(row=0, column=column, padx=10, pady=5)
    
        # Create Offers Menu Frame (Hidden initially)
        self.offers_menu = ctk.CTkFrame(self.root, fg_color="#1F3A68", corner_radius=5, width=200, height=120)  # Set width and height here
    
        options = ["Deals"]
        for i, option in enumerate(options):
            btn = ctk.CTkButton(self.offers_menu, text=option, fg_color="#1F3A68", hover_color="#14284D", 
                            command=lambda opt=option: self.offers_option_selected(opt))
            btn.pack(fill='x', pady=2)

        # Bind hover events
        self.offers_button.bind("<Enter>", self.show_offers_options)
        self.offers_menu.bind("<Enter>", self.cancel_hide_offers_options)
        self.offers_menu.bind("<Leave>", self.schedule_hide_offers_options)
        self.offers_button.bind("<Leave>", self.schedule_hide_offers_options)

    def show_pay_options(self, event=None):
    # Get the position of the PAY button relative to the navigation frame
        x = self.pay_button.winfo_x()  # X coordinate within the navigation frame
        y = self.pay_button.winfo_y() + self.pay_button.winfo_height()  # Y coordinate below the button
    # Place the dropdown menu relative to the navigation frame
        self.pay_menu.place(in_=self.nav_frame, x=x-40, y=y)

    def show_save_options(self, event=None):
        x = self.save_button.winfo_x()
        y = self.save_button.winfo_y() + self.save_button.winfo_height()
        self.save_menu.place(in_=self.nav_frame, x=x-80, y=y)

    def show_invest_options(self, event=None):
        x = self.invest_button.winfo_x()
        y = self.invest_button.winfo_y() + self.invest_button.winfo_height()
        self.invest_menu.place(in_=self.nav_frame, x=x-120, y=y)

    def show_borrow_options(self, event=None):
        x = self.borrow_button.winfo_x()
        y = self.borrow_button.winfo_y() + self.borrow_button.winfo_height()
        self.borrow_menu.place(in_=self.nav_frame, x=x-160, y=y)

    def show_insure_options(self, event=None):
        x = self.insure_button.winfo_x()
        y = self.insure_button.winfo_y() + self.insure_button.winfo_height()
        self.insure_menu.place(in_=self.nav_frame, x=x-200, y=y)

    def show_offers_options(self, event=None):
        x = self.offers_button.winfo_x()
        y = self.offers_button.winfo_y() + self.offers_button.winfo_height()
        self.offers_menu.place(in_=self.nav_frame, x=x-240, y=y)

    def cancel_hide_pay_options(self, event=None):
        # Cancel any pending hide operation
        if hasattr(self, "hide_pay_options_id"):
            self.root.after_cancel(self.hide_pay_options_id)
            del self.hide_pay_options_id

    def cancel_hide_save_options(self, event=None):
        # Cancel any pending hide operation
        if hasattr(self, "hide_save_options_id"):
            self.root.after_cancel(self.hide_save_options_id)
            del self.hide_save_options_id

    def cancel_hide_invest_options(self, event=None):
        # Cancel any pending hide operation
        if hasattr(self, "hide_invest_options_id"):
            self.root.after_cancel(self.hide_invest_options_id)
            del self.hide_invest_options_id

    def cancel_hide_borrow_options(self, event=None):
        # Cancel any pending hide operation
        if hasattr(self, "hide_borrow_options_id"):
            self.root.after_cancel(self.hide_borrow_options_id)
            del self.hide_borrow_options_id

    def cancel_hide_insure_options(self, event=None):
        # Cancel any pending hide operation
        if hasattr(self, "hide_insure_options_id"):
            self.root.after_cancel(self.hide_insure_options_id)
            del self.hide_insure_options_id

    def cancel_hide_offers_options(self, event=None):
        # Cancel any pending hide operation
        if hasattr(self, "hide_offers_options_id"):
            self.root.after_cancel(self.hide_offers_options_id)
            del self.hide_offers_options_id

    def schedule_hide_pay_options(self, event=None):
        # Schedule the hide operation after a delay
        if hasattr(self, "hide_pay_options_id"):
            self.root.after_cancel(self.hide_pay_options_id)
        self.hide_pay_options_id = self.root.after(200, self.hide_pay_options)

    def schedule_hide_save_options(self, event=None):
        # Schedule the hide operation after a delay
        if hasattr(self, "hide_save_options_id"):
            self.root.after_cancel(self.hide_save_options_id)
        self.hide_save_options_id = self.root.after(200, self.hide_save_options)

    def schedule_hide_invest_options(self, event=None):
        # Schedule the hide operation after a delay
        if hasattr(self, "hide_invest_options_id"):
            self.root.after_cancel(self.hide_invest_options_id)
        self.hide_invest_options_id = self.root.after(200, self.hide_invest_options)

    def schedule_hide_borrow_options(self, event=None):
        # Schedule the hide operation after a delay
        if hasattr(self, "hide_borrow_options_id"):
            self.root.after_cancel(self.hide_borrow_options_id)
        self.hide_borrow_options_id = self.root.after(200, self.hide_borrow_options)

    def schedule_hide_insure_options(self, event=None):
        # Schedule the hide operation after a delay
        if hasattr(self, "hide_insure_options_id"):
            self.root.after_cancel(self.hide_insure_options_id)
        self.hide_insure_options_id = self.root.after(200, self.hide_insure_options)

    def schedule_hide_offers_options(self, event=None):
        # Schedule the hide operation after a delay
        if hasattr(self, "hide_offers_options_id"):
            self.root.after_cancel(self.hide_offers_options_id)
        self.hide_offers_options_id = self.root.after(200, self.hide_offers_options)

    def hide_pay_options(self):
        # Hide the pay_menu only if the cursor is not over the button or menu
        if not self.is_cursor_over_pay_button() and not self.is_cursor_over_pay_menu():
            self.pay_menu.place_forget()
            if hasattr(self, "hide_pay_options_id"):
                del self.hide_pay_options_id

    def hide_save_options(self):
        # Hide the save_menu only if the cursor is not over the button or menu
        if not self.is_cursor_over_save_button() and not self.is_cursor_over_save_menu():
            self.save_menu.place_forget()
            if hasattr(self, "hide_save_options_id"):
                del self.hide_save_options_id

    def hide_invest_options(self):
        # Hide the invest_menu only if the cursor is not over the button or menu
        if not self.is_cursor_over_invest_button() and not self.is_cursor_over_invest_menu():
            self.invest_menu.place_forget()
            if hasattr(self, "hide_invest_options_id"):
                del self.hide_invest_options_id

    def hide_borrow_options(self):
        # Hide the borrow_menu only if the cursor is not over the button or menu
        if not self.is_cursor_over_borrow_button() and not self.is_cursor_over_borrow_menu():
            self.borrow_menu.place_forget()
            if hasattr(self, "hide_borrow_options_id"):
                del self.hide_borrow_options_id

    def hide_insure_options(self):
        # Hide the insure_menu only if the cursor is not over the button or menu
        if not self.is_cursor_over_insure_button() and not self.is_cursor_over_insure_menu():
            self.insure_menu.place_forget()
            if hasattr(self, "hide_insure_options_id"):
                del self.hide_insure_options_id

    def hide_offers_options(self):
        # Hide the offers_menu only if the cursor is not over the button or menu
        if not self.is_cursor_over_offers_button() and not self.is_cursor_over_offers_menu():
            self.offers_menu.place_forget()
            if hasattr(self, "hide_offers_options_id"):
                del self.hide_offers_options_id

    def is_cursor_over_pay_button(self):
        # Check if the cursor is over the PAY button
        x, y = self.root.winfo_pointerxy()
        pay_button_x = self.pay_button.winfo_rootx()
        pay_button_y = self.pay_button.winfo_rooty()
        pay_button_width = self.pay_button.winfo_width()
        pay_button_height = self.pay_button.winfo_height()
        
        return (pay_button_x <= x <= pay_button_x + pay_button_width and
                pay_button_y <= y <= pay_button_y + pay_button_height)

    def is_cursor_over_pay_menu(self):
        # Check if the cursor is over the PAY dropdown menu
        x, y = self.root.winfo_pointerxy()
        pay_menu_x = self.pay_menu.winfo_rootx()
        pay_menu_y = self.pay_menu.winfo_rooty()
        pay_menu_width = self.pay_menu.winfo_width()
        pay_menu_height = self.pay_menu.winfo_height()
        
        return (pay_menu_x <= x <= pay_menu_x + pay_menu_width and
                pay_menu_y <= y <= pay_menu_y + pay_menu_height)

    def is_cursor_over_save_button(self):
        # Check if the cursor is over the SAVE button
        x, y = self.root.winfo_pointerxy()
        save_button_x = self.save_button.winfo_rootx()
        save_button_y = self.save_button.winfo_rooty()
        save_button_width = self.save_button.winfo_width()
        save_button_height = self.save_button.winfo_height()
        
        return (save_button_x <= x <= save_button_x + save_button_width and
                save_button_y <= y <= save_button_y + save_button_height)

    def is_cursor_over_save_menu(self):
        # Check if the cursor is over the SAVE dropdown menu
        x, y = self.root.winfo_pointerxy()
        save_menu_x = self.save_menu.winfo_rootx()
        save_menu_y = self.save_menu.winfo_rooty()
        save_menu_width = self.save_menu.winfo_width()
        save_menu_height = self.save_menu.winfo_height()
        
        return (save_menu_x <= x <= save_menu_x + save_menu_width and
                save_menu_y <= y <= save_menu_y + save_menu_height)

    def is_cursor_over_invest_button(self):
        # Check if the cursor is over the INVEST button
        x, y = self.root.winfo_pointerxy()
        invest_button_x = self.invest_button.winfo_rootx()
        invest_button_y = self.invest_button.winfo_rooty()
        invest_button_width = self.invest_button.winfo_width()
        invest_button_height = self.invest_button.winfo_height()
        
        return (invest_button_x <= x <= invest_button_x + invest_button_width and
                invest_button_y <= y <= invest_button_y + invest_button_height)

    def is_cursor_over_invest_menu(self):
        # Check if the cursor is over the INVEST dropdown menu
        x, y = self.root.winfo_pointerxy()
        invest_menu_x = self.invest_menu.winfo_rootx()
        invest_menu_y = self.invest_menu.winfo_rooty()
        invest_menu_width = self.invest_menu.winfo_width()
        invest_menu_height = self.invest_menu.winfo_height()
        
        return (invest_menu_x <= x <= invest_menu_x + invest_menu_width and
                invest_menu_y <= y <= invest_menu_y + invest_menu_height)

    def is_cursor_over_borrow_button(self):
        # Check if the cursor is over the BORROW button
        x, y = self.root.winfo_pointerxy()
        borrow_button_x = self.borrow_button.winfo_rootx()
        borrow_button_y = self.borrow_button.winfo_rooty()
        borrow_button_width = self.borrow_button.winfo_width()
        borrow_button_height = self.borrow_button.winfo_height()
        
        return (borrow_button_x <= x <= borrow_button_x + borrow_button_width and
                borrow_button_y <= y <= borrow_button_y + borrow_button_height)

    def is_cursor_over_borrow_menu(self):
        # Check if the cursor is over the BORROW dropdown menu
        x, y = self.root.winfo_pointerxy()
        borrow_menu_x = self.borrow_menu.winfo_rootx()
        borrow_menu_y = self.borrow_menu.winfo_rooty()
        borrow_menu_width = self.borrow_menu.winfo_width()
        borrow_menu_height = self.borrow_menu.winfo_height()
        
        return (borrow_menu_x <= x <= borrow_menu_x + borrow_menu_width and
                borrow_menu_y <= y <= borrow_menu_y + borrow_menu_height)

    def is_cursor_over_insure_button(self):
        # Check if the cursor is over the INSURE button
        x, y = self.root.winfo_pointerxy()
        insure_button_x = self.insure_button.winfo_rootx()
        insure_button_y = self.insure_button.winfo_rooty()
        insure_button_width = self.insure_button.winfo_width()
        insure_button_height = self.insure_button.winfo_height()
        
        return (insure_button_x <= x <= insure_button_x + insure_button_width and
                insure_button_y <= y <= insure_button_y + insure_button_height)

    def is_cursor_over_insure_menu(self):
        # Check if the cursor is over the INSURE dropdown menu
        x, y = self.root.winfo_pointerxy()
        insure_menu_x = self.insure_menu.winfo_rootx()
        insure_menu_y = self.insure_menu.winfo_rooty()
        insure_menu_width = self.insure_menu.winfo_width()
        insure_menu_height = self.insure_menu.winfo_height()
        
        return (insure_menu_x <= x <= insure_menu_x + insure_menu_width and
                insure_menu_y <= y <= insure_menu_y + insure_menu_height)

    def is_cursor_over_offers_button(self):
        # Check if the cursor is over the OFFERS button
        x, y = self.root.winfo_pointerxy()
        offers_button_x = self.offers_button.winfo_rootx()
        offers_button_y = self.offers_button.winfo_rooty()
        offers_button_width = self.offers_button.winfo_width()
        offers_button_height = self.offers_button.winfo_height()
        
        return (offers_button_x <= x <= offers_button_x + offers_button_width and
                offers_button_y <= y <= offers_button_y + offers_button_height)

    def is_cursor_over_offers_menu(self):
        # Check if the cursor is over the OFFERS dropdown menu
        x, y = self.root.winfo_pointerxy()
        offers_menu_x = self.offers_menu.winfo_rootx()
        offers_menu_y = self.offers_menu.winfo_rooty()
        offers_menu_width = self.offers_menu.winfo_width()
        offers_menu_height = self.offers_menu.winfo_height()
        
        return (offers_menu_x <= x <= offers_menu_x + offers_menu_width and
                offers_menu_y <= y <= offers_menu_y + offers_menu_height)

    def pay_option_selected(self, option):
        option_files = {
            "Money Transfer": "money_transfer.py",
            "Cards": "cards.py",
            "Bill Payments": "bill_payments.py",
            "Recharge": "recharge.py"
        }

        if option in option_files:
            try:
                if option == "Cards":  # Check if the user selected "Cards"
                    subprocess.run(["python", "cards.py", str(logged_in_account_number)])
                elif option == "Bill Payments":
                    subprocess.Popen(["python", "bill_payments.py", logged_in_account_number])
                elif option == "Recharge":
                    subprocess.Popen(["python", "recharge.py", logged_in_account_number])    

                    
                else:
                    subprocess.Popen(["python", option_files[option]])  # Open other files normally
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {option_files[option]}: {str(e)}")
        else:
            messagebox.showinfo("Selected Option", f"You selected: {option}")


    def save_option_selected(self, option):
        option_files = {
            "Accounts": "accounts.py",
            "Deposits": "deposits.py",
            "Locker": "locker.py",
            
        }

        if option in option_files:
            try:
                if option == "Accounts":  # Check if the user selected "Cards"
                    subprocess.run(["python", "accounts.py", str(logged_in_account_number)])
                elif option == "Deposits":
                    subprocess.Popen(["python", "deposits.py", logged_in_account_number])
                elif option == "Locker":
                    subprocess.Popen(["python", "locker.py", logged_in_account_number])    

                    
                else:
                    subprocess.Popen(["python", option_files[option]])  # Open other files normally
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {option_files[option]}: {str(e)}")
        else:
            messagebox.showinfo("Selected Option", f"You selected: {option}")

    def invest_option_selected(self, option):
        option_files = {
            "Bonds": "bonds.py",
            "Mutual Funds": "mf.py",
            
            
        }

        if option in option_files:
            try:
                if option == "Bonds":  # Check if the user selected "Cards"
                    subprocess.run(["python", "bonds.py", str(logged_in_account_number)])
                elif option == "Mutual Funds":
                    subprocess.Popen(["python", "mf.py", str(logged_in_account_number)])
                 
                else:
                    subprocess.Popen(["python", option_files[option]])  # Open other files normally
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {option_files[option]}: {str(e)}")
        else:
            messagebox.showinfo("Selected Option", f"You selected: {option}")

    def insure_option_selected(self, option):
        option_files = {
            "Vehicle": "vehicle.py",
            "Life": "life.py",
            "Health": "health.py",
            
        }

        if option in option_files:
            try:
                if option == "Vehicle":  # Check if the user selected "Cards"
                    subprocess.run(["python", "vehicle.py", str(logged_in_account_number)])
                elif option == "Life":
                    subprocess.Popen(["python", "life.py", str(logged_in_account_number)])
                elif option == "Health":
                    subprocess.Popen(["python", "health.py", str(logged_in_account_number)]) 
                else:
                    subprocess.Popen(["python", option_files[option]])  # Open other files normally
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {option_files[option]}: {str(e)}")
        else:
            messagebox.showinfo("Selected Option", f"You selected: {option}")

    def borrow_option_selected(self, option):
        option_files = {
            "Loans": "loans.py",
            "EMI": "emi.py",
            
            
        }

        if option in option_files:
            try:
                if option == "Loans":  # Check if the user selected "Cards"
                    subprocess.run(["python", "loans.py", str(logged_in_account_number)])
                elif option == "EMI":
                    subprocess.Popen(["python", "emi.py", str(logged_in_account_number)])
                 
                else:
                    subprocess.Popen(["python", option_files[option]])  # Open other files normally
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {option_files[option]}: {str(e)}")
        else:
            messagebox.showinfo("Selected Option", f"You selected: {option}")

    def offers_option_selected(self, option):
        option_files = {
            "Deals": "deals.py",
            
            
            
        }

        if option in option_files:
            try:
                if option == "Deals":  # Check if the user selected "Cards"
                    subprocess.run(["python", "deals.py", str(logged_in_account_number)])
                
                 
                else:
                    subprocess.Popen(["python", option_files[option]])  # Open other files normally
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {option_files[option]}: {str(e)}")
        else:
            messagebox.showinfo("Selected Option", f"You selected: {option}")

    def update_slideshow(self):
        self.current_image = next(self.image_cycle)
        self.display_image(self.current_image)
        self.root.after(5000, self.update_slideshow)  # Change image every 5 seconds
    
    def prev_image(self):
        self.images = [self.images[-1]] + self.images[:-1]  # Rotate list backward
        self.current_image = self.images[0]
        self.display_image(self.current_image)
    
    def next_image(self):
        self.current_image = next(self.image_cycle)
        self.display_image(self.current_image)
    
    def display_image(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((1200, 600))  # Resize image to fit the slideshow frame
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep reference
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def logout(self):
        self.root.destroy()
        import subprocess
        subprocess.run(["python", "login.py"])
        messagebox.showinfo("Logout", "You have logged out successfully!")
        
    

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    username = sys.argv[1] if len(sys.argv) > 1 else "User"
    app = BankingApp(root)
    root.mainloop()
