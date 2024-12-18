import customtkinter as ctk
from tkinter import messagebox
from db_connection import create_connection, close_connection

class RegisterWindow:
    def __init__(self, master, user_data):
        self.master = master
        self.user_data = user_data

        self.window = ctk.CTkToplevel(master)
        self.window.title("Register")
        self.window.geometry("400x400")

        self.label_username = ctk.CTkLabel(self.window, text="Username:")
        self.label_username.pack(pady=10)

        self.entry_username = ctk.CTkEntry(self.window, placeholder_text="Enter Username")
        self.entry_username.pack(pady=10)

        self.label_password = ctk.CTkLabel(self.window, text="Password:")
        self.label_password.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self.window, placeholder_text="Enter Password", show="*")
        self.entry_password.pack(pady=10)

        self.button_register = ctk.CTkButton(self.window, text="Register", command=self.register)
        self.button_register.pack(pady=10)

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        connection = create_connection()
        cursor = connection.cursor()

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, password))
            connection.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error during registration: {e}")

        close_connection(connection)
