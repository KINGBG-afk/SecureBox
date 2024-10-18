from app import SecureBox
import customtkinter as ctk

if __name__ == "__main__":
    win = ctk.CTk()
    app = SecureBox(win)
    win.mainloop()
