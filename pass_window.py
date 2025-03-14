import customtkinter as ctk
from tkinter import messagebox
from encryptor import Cryptor
import os


class PasswordWindow(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk, path: str, name: str, callback) -> None:
        super().__init__(parent)  # child of main app
        self.path = path
        self.name = name
        self.callback = callback
        self.cryptor = Cryptor(self.path, self.name)
        self.master_key = None

        self.geometry("300x100")
        self.resizable(False, False)
        self.title(name)

        self.password_var = ctk.StringVar()
        self.create_ui()

        self.transient(parent)  # make it modal window
        self.grab_set()  # prevent interaction with main window
        self.wait_window(self)  # wait untill this window is closed

    def create_ui(self) -> None:
        self.entry = ctk.CTkEntry(
            self,
            width=190,
            textvariable=self.password_var,
        )

        button = ctk.CTkButton(self, text="Continiue", command=self.confirm_pass)

        self.bind("<Return>", lambda event: self.confirm_pass())

        self.entry.pack(pady=15)
        button.pack()

    def confirm_pass(self) -> bytes | None:
        if os.path.exists(self.path + r"/password/master_key.txt"):
            self.master_key = self.cryptor.unlock_master_key(self.password_var.get())
            if self.master_key:
                self.destroy()
                self.callback(self.master_key)
            return

        else:
            if messagebox.askokcancel(
                self.name,
                "WARNING! You haven't set a password. If you continue, a new password will be created.",
            ):
                self.cryptor.store_password(self.password_var.get())

                self.master_key = self.cryptor.unlock_master_key(
                    self.password_var.get()
                )
                if self.master_key:
                    self.destroy()
                    self.callback(self.master_key)

            return
