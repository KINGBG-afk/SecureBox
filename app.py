import customtkinter as ctk
from tkinter import filedialog, messagebox
from encryptor import Cryptor
import os


class SecureBox:
    def __init__(self, win: ctk.CTk) -> None:
        self.encrypt_flag = False
        self.decrypt_flag = False
        self.saved_flag = True
        self.file_name = None

        self.win = win
        self.win.minsize(400, 300)
        self.win.geometry("1000x700")

        self.path_var = ctk.StringVar()
        self.saved_var = ctk.StringVar()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.win.protocol("WM_DELETE_WINDOW", self.close_program)

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

        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            width=100,
            command=self.encrypt_content,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame, text="Decrypt", width=100, command=self.decrypt_content
        ).pack(side="right", padx=5)

        ctk.CTkButton(left_frame, text="Save", command=self.save_file).pack(fill="x")

        ctk.CTkLabel(left_frame, textvariable=self.saved_var).pack()

        # right frame
        right_frame = ctk.CTkFrame(self.win, width=400, height=400)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.text_field = ctk.CTkTextbox(right_frame)
        self.text_field.pack(fill="both", expand=True)

        # if the user types something mark it as unsaced changes
        self.text_field.bind("<Key>", self.text_change)

        self.win.grid_columnconfigure(1, weight=1)
        self.win.grid_rowconfigure(0, weight=1)

    def text_change(self, event) -> None:
        self.saved_flag = False
        self.saved_var.set("There are unsaved changes")

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

        self.encrypt_flag = False
        self.decrypt_flag = False
        self.file_name = os.path.basename(self.path_var.get())

    def save_file(self) -> None:
        with open(self.path_var.get(), "w") as f:
            f.write(self.text_field.get("1.0", "end"))

        self.saved_flag = True
        self.saved_var.set("")

    def encrypt_content(self) -> None:
        if self.encrypt_flag:
            messagebox.showinfo("SecureBox", "File is already encrypted")

        content = self.cryptor.encrypt_content(
            bytes(self.text_field.get("1.0", "end"), "utf-8"), self.file_name
        )

        self.text_field.delete("1.0", "end")
        self.text_field.insert("1.0", content)

        self.encrypt_flag = True
        self.decrypt_flag = False

        self.saved_flag = False
        self.saved_var.set("There are unsaved changes")

    def decrypt_content(self) -> None:
        if self.decrypt_flag:
            messagebox.showinfo("SecureBox", "File is already decrypted")
            return

        content = self.cryptor.decrypt_content(
            bytes(self.text_field.get("1.0", "end"), "utf-8"), self.file_name
        )

        self.text_field.delete("1.0", "end")
        self.text_field.insert("1.0", content)

        self.encrypt_flag = False
        self.decrypt_flag = True

        self.saved_flag = False
        self.saved_var.set("There are unsaved changes")

    def close_program(self) -> None:
        if not self.saved_flag:
            answer = messagebox.askyesnocancel(
                "SecureBox", "Do you want to save before exit?"
            )

            if answer:
                self.encrypt_content()
                self.save_file()
                self.win.destroy()

            elif not answer:
                self.win.destroy()

    def run(self) -> None:
        self.win.mainloop()


if __name__ == "__main__":
    app = SecureBox(ctk.CTk())
    app.run()
