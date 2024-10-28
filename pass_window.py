import customtkinter as ctk
from tkinter import messagebox
from encryptor import Cryptor
import os


class PasswordWindow:
    def __init__(self, path: str, name: str, callback) -> None:
        self.win = ctk.CTk()
        self.path = path
        self.name = name
        self.callback = callback
        self.cryptor = Cryptor(self.path, self.name)
        self.master_key = None

        self.win.geometry("300x100")
        self.win.resizable(False, False)

        self.password_var = ctk.StringVar()
        self.create_ui()

    def create_ui(self) -> None:
        self.entry = ctk.CTkEntry(
            self.win,
            width=190,
            textvariable=self.password_var,
        ).pack(pady=15)

        ctk.CTkButton(self.win, text="Continiue", command=self.confirm_pass).pack()
        self.win.bind("<Return>", lambda event: self.confirm_pass())

    def confirm_pass(self) -> bytes | None:
        if os.path.exists(self.path + r"/password/master_key.txt"):
            self.master_key = self.cryptor.unlock_master_key(self.password_var.get())
            if self.master_key:
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
                    self.callback(self.master_key)
            return

    def run(self) -> None:
        self.win.mainloop()

    def close(self) -> None:
        self.win.quit()
        self.win.destroy()


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    a = PasswordWindow(path, "SecureBox", lambda x: print(f"Done {x}"))
    a.run()
