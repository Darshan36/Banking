import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import bcrypt
import requests
import random
from PIL import Image, ImageTk
import subprocess

# Initialize CustomTkinter Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="FWbdT#R2",
    database="banking_system"
)
cursor = db.cursor()


# OTP API Key
MAILERSEND_API_KEY = "mlsn.3d0ccaeaf2d2c85bf866d2ac18332bd0e2a28f0c356fbc30e913fc83e97a9cc4"

# Password Hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# Send OTP Function
def send_otp(email):
    global generated_otp
    generated_otp = str(random.randint(100000, 999999))
    url = "https://api.mailersend.com/v1/email"
    headers = {"Authorization": f"Bearer {MAILERSEND_API_KEY}", "Content-Type": "application/json"}
    data = {"from": {"email": "MS_czrkAr@trial-x2p0347nx03lzdrn.mlsender.net"},
            "to": [{"email": email}], "subject": "Your OTP Code", "text": f"Your OTP is {generated_otp}"}
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 202:
        return generated_otp
    else:
        return None

# Open Registration Window
def open_register():
    reg_window = ctk.CTkToplevel(root)
    reg_window.title("Register")
    reg_window.geometry("400x500")
    reg_window.attributes('-topmost', True)

    ctk.CTkLabel(reg_window, text="Register", font=("Arial", 20, "bold")).pack(pady=10)

    global entry_reg_username, entry_reg_password, entry_reg_email, entry_reg_mpin

    entry_reg_username = ctk.CTkEntry(reg_window, placeholder_text="Username", width=300)
    entry_reg_username.pack(pady=5)

    entry_reg_password = ctk.CTkEntry(reg_window, placeholder_text="Password", show="*", width=300)
    entry_reg_password.pack(pady=5)

    entry_reg_email = ctk.CTkEntry(reg_window, placeholder_text="Email", width=300)
    entry_reg_email.pack(pady=5)

    entry_reg_mpin = ctk.CTkEntry(reg_window, placeholder_text="MPIN (4-digit)", show="*", width=300)
    entry_reg_mpin.pack(pady=5)

    ctk.CTkButton(reg_window, text="Register", command=register, fg_color="green").pack(pady=10)

# Registration Function
def register():
    username = entry_reg_username.get()
    password = entry_reg_password.get()
    email = entry_reg_email.get()
    mpin = entry_reg_mpin.get()

    if not username or not password or not email or not mpin:
        messagebox.showerror("Error", "All fields are required!")
        return

    if not mpin.isdigit() or len(mpin) != 4:
        messagebox.showerror("Error", "MPIN must be a 4-digit number!")
        return

    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, email, mpin) VALUES (%s, %s, %s, %s)",
                       (username, hashed_password, email, mpin))
        db.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Registration failed: {err}")


def generate_account_number():
    """Generate a random 10-digit account number."""
    return random.randint(10**9, (10**10) - 1)

def is_account_number_unique(account_number):
    """Check if the account number already exists in the database."""
    cursor.execute("SELECT account_number FROM accounts WHERE account_number = %s", (account_number,))
    return cursor.fetchone() is None  # True if unique, False if duplicate

def assign_account_number(username):
    """Assign a unique 10-digit account number to the user."""
    while True:
        account_number = generate_account_number()  # Generate a random account number
        if is_account_number_unique(account_number):  # Check if it's unique
            break  # Exit the loop if the account number is unique

    # Insert the account number into the database
    try:
        cursor.execute("INSERT INTO accounts (username, account_number) VALUES (%s, %s)", (username, account_number))
        db.commit()
        return account_number
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to assign account number: {err}")
        return None

# Login Function
import mysql.connector
import subprocess
import customtkinter as ctk
from tkinter import messagebox

def login():
    username = entry_login_username.get()
    password = entry_login_password.get()
    mpin = entry_login_mpin.get()
    otp = entry_login_otp.get()

    cursor.execute("SELECT password, email, mpin FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        stored_password, email, stored_mpin = user
        if verify_password(stored_password, password) and stored_mpin == mpin:
            if otp == generated_otp:
                # Fetch account number from accounts table
                cursor.execute("SELECT account_number FROM accounts WHERE username = %s", (username,))
                account_data = cursor.fetchone()

                if account_data:
                    logged_in_account_number = str(account_data[0])  # Store the account number
                    messagebox.showinfo("Login Successful", f"Welcome, {username}\nYour account number: {logged_in_account_number}")

                    # Pass account number to dashboard.py
                    subprocess.run(["python", "dashboard.py",logged_in_account_number])
                    root.destroy()
                else:
                    messagebox.showerror("Error", "No account found for this user!")
            else:
                messagebox.showerror("Error", "Invalid OTP!")
        else:
            messagebox.showerror("Error", "Invalid password or MPIN!")
    else:
        messagebox.showerror("Error", "User not found!")


# OTP Request Function
def request_otp():
    username = entry_login_username.get()
    cursor.execute("SELECT email FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        email = user[0]
        send_otp(email)
        messagebox.showinfo("Success", "OTP sent to your email!")
    else:
        messagebox.showerror("Error", "User not found!")

# Main Login Window
root = ctk.CTk()
root.title("Banking System")
root.geometry("1920x1080")  
root.state("zoomed")  

# Load and set the background image
original_image = Image.open("Welcome.png")  
bg_label = ctk.CTkLabel(root, text="")
bg_label.place(relwidth=1, relheight=1)

def update_bg(event=None):
    """Resize and update the background image."""
    new_width, new_height = root.winfo_width(), root.winfo_height()
    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized_image)
    bg_label.configure(image=bg_photo)
    bg_label.image = bg_photo  # Keep reference

# Bind the window resizing event
root.bind("<Configure>", update_bg)
update_bg()  

# Login Frame
frame = ctk.CTkFrame(root, width=450, height=500, corner_radius=15, fg_color="#222")
frame.place(relx=0.71, rely=0.5, anchor="center")

ctk.CTkLabel(frame, text="Sign In", font=("Arial", 40, "bold")).pack(pady=20)

entry_login_username = ctk.CTkEntry(frame, placeholder_text="Username", width=300)
entry_login_username.pack(pady=10)

entry_login_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300)
entry_login_password.pack(pady=10)

entry_login_mpin = ctk.CTkEntry(frame, placeholder_text="MPIN (4-digit)", show="*", width=300)
entry_login_mpin.pack(pady=10)

entry_login_otp = ctk.CTkEntry(frame, placeholder_text="Enter OTP", width=300)
entry_login_otp.pack(pady=10)

ctk.CTkButton(frame, text="Request OTP", command=request_otp, fg_color="blue").pack(pady=5)
ctk.CTkButton(frame, text="Login", command=login, fg_color="green").pack(pady=5)
ctk.CTkButton(frame, text="Register", command=open_register, fg_color="gray").pack(pady=5)

# Start main event loop
root.mainloop()
