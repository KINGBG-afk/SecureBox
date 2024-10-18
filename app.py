import customtkinter as ctk
from tkinter import filedialog
from encryptor import Cryptor
import os


class SecureBox:
    def __init__(self, win: ctk.CTk) -> None:
        self.win = win
        self.win.minsize(400, 300)
        self.win.geometry("1000x700")
        self.path_var = ctk.StringVar()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.cryptor = Cryptor(os.path.dirname(os.path.abspath(__file__)))
        self.create_ui()

    def create_ui(self) -> None:
        # left frame
        left_frame = ctk.CTkFrame(self.win, width=200, height=400)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        directory_entry = ctk.CTkEntry(
            left_frame, placeholder_text="Enter directory", textvariable=self.path_var
        )
        directory_entry.pack(pady=10)

        ctk.CTkButton(left_frame, text="Search", command=self.open_file).pack(pady=10)

        button_frame = ctk.CTkFrame(left_frame)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Crypt", width=100).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="Decrypt", width=100).pack(
            side="right", padx=5
        )

        ctk.CTkButton(left_frame, text="save", command=self.save_file).pack(fill="x")

        # right frame
        right_frame = ctk.CTkFrame(self.win, width=400, height=400)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.text_field = ctk.CTkTextbox(right_frame)
        self.text_field.pack(fill="both", expand=True)

        self.win.grid_columnconfigure(1, weight=1)
        self.win.grid_rowconfigure(0, weight=1)

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )
        self.path_var.set(file_path)

        with open(file_path, "r") as f:
            content = f.read()
            self.text_field.delete("1.0", "end")
            self.text_field.insert("1.0", content)

    def save_file(self) -> None:
        with open(self.path_var.get(), "w") as f:
            f.write(self.text_field.get("1.0", "end"))


if __name__ == "__main__":
    win = ctk.CTk()
    app = SecureBox(win)
    win.mainloop()
