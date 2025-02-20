import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tkinter import * 
from tkinter import font
from tkinter import messagebox
from my_chatbot import chat, clear_chat_history, chatbot_data
from PIL import Image, ImageTk

BG_MAIN = "#275aa9" #rgb(39, 90, 169)
BG_CHAT = "#f8f8f8"
BG_CHATBOT = "#2b2b2b"
TEXT_COLOR = "#000000"
SEND_BUTTON = "#3371D0"

FONT = ("Segoe UI", 14)
FONT_BOLD = ("Segoe UI", 14, "bold")

CLEAR_HISTORY_IMAGE = "./assets/clear_history.png"
CHATBOT_IMAGE = "./assets/chatbot_image.png"
EXPORT_IMAGE = "./assets/export_icon.png"


class ChatBotGui:
    def __init__(self):
        self.window = Tk()
        self.export_image = self.prepare_image(EXPORT_IMAGE, 70,70)
        self.chatbot_image = self.prepare_image(CHATBOT_IMAGE, 60, 70)
        self.clear_history_image = self.prepare_image(CLEAR_HISTORY_IMAGE, 50, 50)
        self.main_window()

    def prepare_image(self, img_path, width, height):
        img = Image.open(img_path)
        img = img.resize((width, height))
        img = ImageTk.PhotoImage(img)

        return img


    def run(self):
        self.window.mainloop()

    def main_window(self):
        self.window.title("AI Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=500, height=600, bg=BG_MAIN)

        head_label = Label(self.window, bg=BG_MAIN, fg=BG_CHAT,
                           text="Chatty Patty", font=FONT_BOLD, pady=15, padx=15)
        head_label.place(relwidth=1, relheight=0.125, rely=-0.01, relx=.05)

        text_frame = Frame(self.window, bg=BG_CHAT)
        text_frame.place(relheight=0.7, relwidth=1, rely=0.12)

        self.text_widget = Text(text_frame, width=20, height=2, bg=BG_CHAT, 
                                 fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        bottom_label = Label(self.window, bg=BG_MAIN, height=80)
        bottom_label.place(relwidth=1, rely=0.82)

        self.text_entry = Entry(bottom_label, bg=BG_CHAT, fg=TEXT_COLOR, font=FONT, bd =0)
        self.text_entry.place(relwidth=0.7, relheight=0.06, rely=0.0125, relx=0.025)
        self.text_entry.focus()
        self.text_entry.bind("<Return>", self.enter_pressed)

        send_button = Button(bottom_label, text="Send\n[Enter]", font=FONT_BOLD,
                             width=20, bg=SEND_BUTTON, fg=BG_CHAT, highlightthickness =0, bd =0,
                             command=lambda: self.enter_pressed(None))
        send_button.place(relx=0.775, rely=0.0125, relheight=0.06, relwidth=0.20)

        clear_button = Button(head_label, image=self.clear_history_image, command=self.clear_history, highlightthickness =0, bd =0)
        clear_button.place(relx = 0.8, rely= 0.22, height = 50, width = 50)

        ai_profile_picture = Label(head_label, image=self.chatbot_image, bd=1)
        ai_profile_picture.place(relx = 0.275, rely= 0.22, height = 50, width = 50)


    def enter_pressed(self, event):
        text = self.text_entry.get()
        self.insert_message(text, "You")

    def insert_message(self, msg, user):
        if not msg:
            return
        
        self.text_entry.delete(0, END)
        sender_msg = f"{user}: {msg}\n\n"

        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, sender_msg)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        recipient_msg = f"{chatbot_data.name}: {chat(msg)}\n\n"

        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, recipient_msg)
        self.text_widget.see(END)
        self.text_widget.configure(state=DISABLED)

    def clear_history(self):
        response = messagebox.askyesno("Confirm", "Are you sure you want to delete all conversation history with the chatbot?" )
        if response:
            print("Conversation history has been deleted.")
            clear_chat_history()

if __name__ == "__main__":
    gui = ChatBotGui()
    gui.run()
