import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class HealthMetricsFrame(ctk.CTkFrame):
    def __init__(self, master, username, connection, go_back_callback):
        super().__init__(master)

        self.master = master
        self.username = username
        self.connection = connection
        self.go_back_callback = go_back_callback

        # Title
        self.label_title = ctk.CTkLabel(self, text="Fill Health Metrics", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=20)

        # Input fields
        self.label_date = ctk.CTkLabel(self, text="Date (YYYY-MM-DD):")
        self.label_date.pack(pady=5)
        self.entry_date = ctk.CTkEntry(self, placeholder_text="Enter date (YYYY-MM-DD)")
        self.entry_date.pack(pady=5)

        self.label_blood_sugar = ctk.CTkLabel(self, text="Blood Sugar (mg/dL):")
        self.label_blood_sugar.pack(pady=5)
        self.entry_blood_sugar = ctk.CTkEntry(self)
        self.entry_blood_sugar.pack(pady=5)

        self.label_cholesterol = ctk.CTkLabel(self, text="Cholesterol (mg/dL):")
        self.label_cholesterol.pack(pady=5)
        self.entry_cholesterol = ctk.CTkEntry(self)
        self.entry_cholesterol.pack(pady=5)

        self.label_uric_acid = ctk.CTkLabel(self, text="Uric Acid (mg/dL):")
        self.label_uric_acid.pack(pady=5)
        self.entry_uric_acid = ctk.CTkEntry(self)
        self.entry_uric_acid.pack(pady=5)

        self.label_heart_rate = ctk.CTkLabel(self, text="Heart Rate (bpm):")
        self.label_heart_rate.pack(pady=5)
        self.entry_heart_rate = ctk.CTkEntry(self)
        self.entry_heart_rate.pack(pady=5)

        self.label_blood_pressure = ctk.CTkLabel(self, text="Blood Pressure (mmHg):")
        self.label_blood_pressure.pack(pady=5)
        self.entry_blood_pressure = ctk.CTkEntry(self)
        self.entry_blood_pressure.pack(pady=5)

        # Buttons
        self.button_submit = ctk.CTkButton(self, text="Submit", command=self.submit_metrics)
        self.button_submit.pack(pady=10)

        self.button_back = ctk.CTkButton(self, text="Back to Menu", command=self.go_back)
        self.button_back.pack(pady=10)

    def submit_metrics(self):
        date = self.entry_date.get()
        blood_sugar = self.entry_blood_sugar.get()
        cholesterol = self.entry_cholesterol.get()
        uric_acid = self.entry_uric_acid.get()
        heart_rate = self.entry_heart_rate.get()
        blood_pressure = self.entry_blood_pressure.get()

        # Validation
        if not date or not blood_sugar or not cholesterol or not uric_acid or not heart_rate or not blood_pressure:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Check if the date is valid
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        cursor = self.connection.cursor()

        # Fetch user ID from the username
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found!")
            return

        user_id = user[0]

        # Insert into database
        query = """
        INSERT INTO health_metrics (user_id, date, blood_sugar, cholesterol, uric_acid, heart_rate, blood_pressure)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (user_id, date, blood_sugar, cholesterol, uric_acid, heart_rate, blood_pressure))
            self.connection.commit()
            messagebox.showinfo("Success", "Health metrics added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            cursor.close()

    def go_back(self):
        self.go_back_callback()
