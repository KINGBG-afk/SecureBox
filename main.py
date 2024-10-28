from app import SecureBox
import customtkinter as ctk
from pass_window import PasswordWindow
import os


if __name__ == "__main__":

    def check_master_key(result: bytes) -> None:
        if result:
            passwin.close()
            app = SecureBox(ctk.CTk(), result)
            app.run()

    passwin = PasswordWindow(os.getcwd(), "SecureBox", check_master_key)
    passwin.run()
