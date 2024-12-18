import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime


class CheckHealthMetricsFrame(ctk.CTkFrame):
    def __init__(self, master, username, connection, go_back_callback):
        super().__init__(master)

        self.master = master
        self.username = username
        self.connection = connection
        self.go_back_callback = go_back_callback

        # Title
        self.label_title = ctk.CTkLabel(self, text="Check Health Metrics", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=20)

        # Calendar for date selection
        self.label_date = ctk.CTkLabel(self, text="Select a Date:")
        self.label_date.pack(pady=10)
        self.calendar = Calendar(self, date_pattern="MM/dd/yyyy")  # Calendar outputs date in MM/DD/YYYY format
        self.calendar.pack(pady=10)

        # Buttons
        self.button_view = ctk.CTkButton(self, text="View Metrics", command=self.view_metrics)
        self.button_view.pack(pady=10)

        self.button_back = ctk.CTkButton(self, text="Back to Menu", command=self.go_back)
        self.button_back.pack(pady=10)

        # Display area
        self.text_output = ctk.CTkTextbox(self, height=15, state="disabled")
        self.text_output.pack(pady=10, fill="both", expand=True)

    def view_metrics(self):
        selected_date = self.calendar.get_date()  # Get date in MM/DD/YYYY format
        try:
            # Convert selected date to YYYY-MM-DD format
            formatted_date = datetime.strptime(selected_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format selected.")
            return

        cursor = self.connection.cursor()

        # Fetch user ID from the username
        cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found!")
            return

        user_id = user[0]

        # Query health metrics for the selected date
        query = """
        SELECT date, blood_sugar, cholesterol, uric_acid, heart_rate, blood_pressure
        FROM health_metrics
        WHERE user_id = %s AND date = %s
        """
        cursor.execute(query, (user_id, formatted_date))
        metrics = cursor.fetchone()

        if metrics:
            # Display metrics
            output = f"Date: {metrics[0]}\n" \
                     f"Blood Sugar: {metrics[1]} mg/dL\n" \
                     f"Cholesterol: {metrics[2]} mg/dL\n" \
                     f"Uric Acid: {metrics[3]} mg/dL\n" \
                     f"Heart Rate: {metrics[4]} bpm\n" \
                     f"Blood Pressure: {metrics[5]}\n"
            self.text_output.configure(state="normal")
            self.text_output.delete("1.0", "end")
            self.text_output.insert("end", output)
            self.text_output.configure(state="disabled")
        else:
            messagebox.showinfo("Info", "No health metrics found for the selected date.")
        cursor.close()

    def go_back(self):
        self.go_back_callback()
