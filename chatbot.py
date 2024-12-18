import requests
import customtkinter as ctk

class ChatbotFrame(ctk.CTkFrame):
    def __init__(self, master, show_main_menu):
        super().__init__(master)
        self.master = master
        self.show_main_menu = show_main_menu

        # Frame Layout
        self.pack(fill="both", expand=True)

        # Chatbox UI
        self.chat_area = ctk.CTkTextbox(self, wrap="word", height=400, width=600)
        self.chat_area.pack(pady=20)
        self.chat_area.insert("1.0", "Chatbot: Hello! How can I assist you today?\n")
        
        # User Input Field
        self.user_input = ctk.CTkEntry(self, placeholder_text="Type your message here")
        self.user_input.pack(pady=10)

        # Send Button
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.show_main_menu)
        self.back_button.pack(pady=10)

    def send_message(self):
        user_message = self.user_input.get()
        if not user_message:
            return

        self.chat_area.insert("end", f"You: {user_message}\n")
        self.user_input.delete(0, "end")

        # Get response from chatbot API
        bot_response = self.get_bot_response(user_message)
        self.chat_area.insert("end", f"Bot: {bot_response}\n")
        self.chat_area.yview("end")

    def get_bot_response(self, user_message):
        # API details
        url = "https://chatgpt-42.p.rapidapi.com/conversationllama3"
        headers = {
            "x-rapidapi-key": "f3e3354db9msh9b38eec5b148c89p169645jsnfd1210887fe5",
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [{"role": "user", "content": user_message}],
            "web_access": False
        }

        try:
            # Make the API request
            response = requests.post(url, json=payload, headers=headers)

            # Debugging: Print status code and response data in the terminal
            print(f"API Status Code: {response.status_code}")
            if response.status_code == 200:
                response_data = response.json()
                print(f"API Response: {response_data}")  # Check the raw response

                # Check if response has the expected 'result' field
                if "result" in response_data:
                    return response_data["result"]
                else:
                    return "Sorry, I couldn't process your query. Please try again."
            else:
                return f"Error: API returned status code {response.status_code}"

        except Exception as e:
            # Error handling
            print(f"Error: {str(e)}")
            return f"Error: {str(e)}"
