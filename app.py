import os
from tkinter import filedialog, messagebox

import customtkinter as ctk
from docx_reader import WordFileReader
from encryptor import Cryptor


class SecureBox:
    def __init__(self, win: ctk.CTk, result: bytes) -> None:
        self.master_key = result

        path = os.path.dirname(os.path.abspath(__file__))
        self.program_name = self.__class__.__name__

        self.encrypt_flag = False
        self.decrypt_flag = False
        self.saved_flag = True
        self.file_name = None
        self.file_path = None

        self.win = win
        self.win.minsize(400, 300)
        self.win.geometry("1000x700")

        self.path_var = ctk.StringVar(self.win)
        self.saved_var = ctk.StringVar(self.win, "")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.win.protocol("WM_DELETE_WINDOW", self.close_program)

        self.cryptor = Cryptor(path, self.program_name)
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

        self.saved_label = ctk.CTkLabel(left_frame, textvariable=self.saved_var)
        self.saved_label.pack()

        # right frame
        right_frame = ctk.CTkFrame(self.win, width=400, height=400)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.text_field = ctk.CTkTextbox(right_frame)
        self.text_field.pack(fill="both", expand=True)

        # if the user types something mark it as unsaced changes
        self.text_field.bind("<Key>", self.text_change)
        self.text_field.bind("<Control-s>", self.save_file, add=True)

        self.win.grid_columnconfigure(1, weight=1)
        self.win.grid_rowconfigure(0, weight=1)

    def text_change(self, *_) -> None:
        self.saved_flag = False
        self.saved_var.set("There are unsaved changes")

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("All Files", "*.*"),),
        )

        if not file_path:
            return

        if not self.saved_flag:
            if not (
                messagebox.askyesno(
                    self.program_name,
                    "You have unsaved changes, are you sure you want to open a new file?",
                )
            ):
                return

        self.path_var.set(file_path)
        self.file_path = self.path_var.get()
        self.file_name = os.path.basename(file_path)

        if self.file_name.split(".")[1] == "docx":
            content = WordFileReader.read_file(file_path)

            # add \n or \n\n to the right places
            for i in range(len(content)):
                if content[i] == "":
                    if i > 0 and content[i - 1] in ["\n\n", "\n"]:
                        content[i] = "\n"
                    else:
                        content[i] = "\n\n"

            # add \n between strings
            i = 0
            while i < len(content) - 1:
                if content[i] not in ["\n\n", "\n", ""] and content[i + 1] not in [
                    "\n\n",
                    "\n",
                    "",
                ]:
                    content.insert(i + 1, "\n")
                    i += 1
                i += 1

            content = [line.replace("\t", "    ") for line in content]

            self.text_field.delete("1.0", "end")
            self.text_field.insert("1.0", "".join(content))

        else:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_field.delete("1.0", "end")
                self.text_field.insert("1.0", content)

        self.encrypt_flag = False
        self.decrypt_flag = False

    def save_file(self, *_) -> None:
        if self.file_path is None or not os.path.exists(self.file_path):
            _file = filedialog.asksaveasfile(
                defaultextension=".txt",
                filetypes=(("All Files", ".*"),),
            )

            if _file:
                text = self.text_field.get("1.0", "end")
                _file.write(text)
                _file.close()

            return

        if self.file_name.split(".")[1] == "docx":
            content = self.text_field.get("1.0", "end-1c").splitlines()
            WordFileReader.write_file(self.file_path, content)

        else:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(self.text_field.get("1.0", "end"))

        self.saved_flag = True
        self.saved_var.set("")

    def encrypt_content(self) -> None:
        if self.encrypt_flag:
            messagebox.showinfo(self.program_name, "File is already encrypted")
            return

        content = self.cryptor.encrypt_content(
            bytes(self.text_field.get("1.0", "end"), "utf-8"), self.master_key
        )

        self.text_field.delete("1.0", "end")
        self.text_field.insert("1.0", content)

        self.encrypt_flag = True
        self.decrypt_flag = False

        self.saved_flag = False
        self.saved_var.set("There are unsaved changes")

    def decrypt_content(self) -> None:
        if self.decrypt_flag:
            messagebox.showinfo(self.program_name, "File is already decrypted")
            return

        content = self.cryptor.decrypt_content(
            bytes(self.text_field.get("1.0", "end"), "utf-8"), self.master_key
        )

        content = content.decode("utf-8")

        self.text_field.delete("1.0", "end")
        self.text_field.insert("1.0", content)

        self.encrypt_flag = False
        self.decrypt_flag = True

        self.saved_flag = False
        self.saved_var.set("There are unsaved changes")

    def close_program(self) -> None:
        if not self.saved_flag:
            answer = messagebox.askyesnocancel(
                self.program_name, "Do you want to save before exit?"
            )

            if answer:
                self.save_file()
                exit()

            elif not answer:
                exit()

        exit()

    def run(self) -> None:
        self.win.mainloop()
