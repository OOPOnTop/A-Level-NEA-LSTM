import customtkinter as ctk


class BlankSpace(ctk.CTkFrame):
    def __init__(self, parent, width, bg, height=None):
        super().__init__(parent)
        if height is None:
            self.blank_space = ctk.CTkLabel(self, text='', bg_color=bg, width=width)
        else:
            self.blank_space = ctk.CTkLabel(self, text='', bg_color=bg, width=width, height=height)
        self.blank_space.grid(row=0, column=0)
