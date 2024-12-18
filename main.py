import customtkinter as ctk
from tkinter import messagebox
from health_metrics import HealthMetricsFrame
from check_health_metrics import CheckHealthMetricsFrame
from chatbot import ChatbotFrame
from register import RegisterWindow
from db_connection import create_connection, close_connection

class CyberFitCoachApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CyberFit Coach")
        self.geometry("700x800")
        self.resizable(False, False)

        # Initialize database connection and user data
        self.connection = create_connection()
        self.user_data = None
        self.username = None

        # Start with the login page
        self.show_login_page()

    def show_login_page(self):
        self.clear_window()

        self.label_title = ctk.CTkLabel(self, text="CyberFit Coach", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Enter Username")
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Enter Password", show="*")
        self.entry_password.pack(pady=10)

        self.button_login = ctk.CTkButton(self, text="Login", command=self.login)
        self.button_login.pack(pady=10)

        self.button_register = ctk.CTkButton(self, text="Register", command=self.show_register_window)
        self.button_register.pack(pady=10)

    def show_register_window(self):
        RegisterWindow(self, self.connection)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in both username and password!")
            return

        cursor = self.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            self.username = username
            self.user_data = {"id": user[0], "username": user[1]}
            messagebox.showinfo("Success", "Login successful!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

        cursor.close()

    def show_main_menu(self):
        self.clear_window()

        self.label_title = ctk.CTkLabel(self, text=f"Welcome, {self.username}", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        self.button_fill_metrics = ctk.CTkButton(self, text="Fill Health Metrics", command=self.show_health_metrics)
        self.button_fill_metrics.pack(pady=10)

        self.button_check_metrics = ctk.CTkButton(self, text="Check Health Metrics", command=self.show_check_metrics)
        self.button_check_metrics.pack(pady=10)

        self.button_chatbot = ctk.CTkButton(self, text="Chatbot", command=self.show_chatbot)
        self.button_chatbot.pack(pady=10)

        self.button_logout = ctk.CTkButton(self, text="Logout", command=self.logout)
        self.button_logout.pack(pady=10)

    def show_health_metrics(self):
        self.clear_window()
        HealthMetricsFrame(self, self.username, self.connection, self.show_main_menu).pack(fill="both", expand=True)

    def show_check_metrics(self):
        self.clear_window()
        CheckHealthMetricsFrame(self, self.username, self.connection, self.show_main_menu).pack(fill="both", expand=True)

    def show_chatbot(self):
        """Navigate to ChatbotFrame and pass required parameters."""
        self.clear_window()
        ChatbotFrame(self, self.show_main_menu).pack(fill="both", expand=True)

    def logout(self):
        self.username = None
        self.user_data = None
        messagebox.showinfo("Logout", "You have successfully logged out.")
        self.show_login_page()

    def clear_window(self):
        """Clear all widgets from the current frame."""
        for widget in self.winfo_children():
            widget.destroy()

    def on_closing(self):
        """Handle the closing of the application."""
        if self.connection:
            close_connection(self.connection)
        self.destroy()

if __name__ == "__main__":
    app = CyberFitCoachApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
