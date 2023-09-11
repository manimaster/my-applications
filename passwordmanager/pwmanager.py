import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import os

# File to store encrypted passwords
PASSWORDS_FILE = 'passwords.txt'
# File to store the encryption key
KEY_FILE = 'key.key'


# Ensure the encryption key exists
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
else:
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()

cipher = Fernet(key)


def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()


def save_password(service, username, password):
    with open(PASSWORDS_FILE, 'a') as f:
        f.write(f"{service} | {username} | {encrypt_password(password)}\n")


def get_password(service):
    if not os.path.exists(PASSWORDS_FILE):
        return None

    with open(PASSWORDS_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(" | ")
            if parts[0] == service:
                return parts[1], decrypt_password(parts[2])
    return None


class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")

        # UI for saving password
        self.service_label = tk.Label(self, text="Service/Website:")
        self.service_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        
        self.service_entry = tk.Entry(self, width=40)
        self.service_entry.grid(row=1, column=0, columnspan=2, padx=20)

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=2, column=0, padx=20, pady=10)
        
        self.username_entry = tk.Entry(self, width=40)
        self.username_entry.grid(row=3, column=0, columnspan=2, padx=20)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=4, column=0, padx=20, pady=10)
        
        self.password_entry = tk.Entry(self, width=40)
        self.password_entry.grid(row=5, column=0, columnspan=2, padx=20)

        self.save_button = tk.Button(self, text="Save Password", command=self.save)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=20)

        # UI for retrieving password
        self.get_password_button = tk.Button(self, text="Retrieve Password", command=self.retrieve)
        self.get_password_button.grid(row=7, column=0, columnspan=2, pady=20)

    def save(self):
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not service or not username or not password:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        save_password(service, username, password)
        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Password saved successfully!")

    def retrieve(self):
        service = simpledialog.askstring("Retrieve Password", "Enter Service/Website:")
        if service:
            credentials = get_password(service)
            if credentials:
                username, password = credentials
                messagebox.showinfo("Credentials", f"Username: {username}\nPassword: {password}")
            else:
                messagebox.showerror("Error", "No credentials found for the given service/website!")


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
