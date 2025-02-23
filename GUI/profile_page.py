import customtkinter as ctk
import gui_settings as settings


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # setting colours
        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        # configure rows and columns
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

        self.profile_title = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=35,
                                          fg_color=settings.ACTIVE_BUTTON_COL, text='Profile', width=200,
                                          font=(settings.PRIMARY_FAMILY, 28, 'bold'))
        self.profile_title.grid(row=0, column=1)

        self.label = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=35,
                                  fg_color=settings.ACTIVE_BUTTON_COL, text='To be added in a future update', width=200,
                                  font=(settings.PRIMARY_FAMILY, 22))
        self.label.grid(row=1, column=1, pady=50)

