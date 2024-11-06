from app import SecureBox
import customtkinter as ctk
from pass_window import PasswordWindow
import os


if __name__ == "__main__":

    def check_master_key(result: bytes) -> None:
        if result:
            app = SecureBox(ctk.CTk(), result)
            passwin.close()
            app.run()

    passwin = PasswordWindow(
        os.path.dirname(os.path.abspath(__file__)), "SecureBox", check_master_key
    )

    passwin.run()

