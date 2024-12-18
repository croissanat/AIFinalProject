import customtkinter as ctk
import mysql.connector
from mysql.connector import Error

class AuthFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_health_metrics):
        super().__init__(master)
        self.master = master
        self.switch_to_health_metrics = switch_to_health_metrics
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Login to CyberFit Coach")
        self.label.pack(pady=20)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10)

        self.button_login = ctk.CTkButton(self, text="Login", command=self.login)
        self.button_login.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Database connection
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="fitcoach")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        connection.close()

        if user:
            self.switch_to_health_metrics(username)
        else:
            self.show_warning("Invalid username or password!")

    def show_warning(self, message):
        self.warning_label = ctk.CTkLabel(self, text=message, fg_color="red")
        self.warning_label.pack(pady=10)

