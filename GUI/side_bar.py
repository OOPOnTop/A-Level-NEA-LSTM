import customtkinter as ctk
from GUI import gui_settings as settings
from Home_screen_frame import HomeScreen
from profile_page import ProfileFrame
from Settings import SettingsFrame
from upload_frame import UploadFrame
from suggestion_frame import SuggestionFrame

ROWS = 5
COLUMNS = 1


class SideBar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        for i in range(ROWS):
            self.rowconfigure(i, weight=0)
        for i in range(COLUMNS):
            self.columnconfigure(i, weight=0)

        self.configure(width=250)
        self.configure(fg_color=settings.RECENTLY_PLAYED_COL)
        self.configure(bg_color=settings.BG_COL)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.menu_title = ctk.CTkLabel(self, text='MENU', text_color=(settings.TEXT_COL[0], '#ffffff'), corner_radius=10,
                                       bg_color=settings.RECENTLY_PLAYED_COL, font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                       width=250, anchor='n')

        self.menu_title.grid(row=0, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.home_button =  ctk.CTkButton(self, text_color=(settings.TEXT_COL[0], '#ffffff'), text='Home',
                                          font=(settings.PRIMARY_FAMILY, 20), bg_color=settings.RECENTLY_PLAYED_COL,
                                          width=250, corner_radius=0, fg_color=settings.RECENTLY_PLAYED_COL,
                                          command=lambda: controller.show_frame(HomeScreen))

        self.home_button.grid(row=1, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.suggestions = ctk.CTkButton(self, text_color=(settings.TEXT_COL[0], '#ffffff'), text='Suggestions',
                                         font=(settings.PRIMARY_FAMILY, 20), bg_color=settings.RECENTLY_PLAYED_COL,
                                         width=250, corner_radius=0, fg_color=settings.RECENTLY_PLAYED_COL,
                                         command=lambda: controller.show_frame(SuggestionFrame))

        self.suggestions.grid(row=2, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.upload = ctk.CTkButton(self, text_color=(settings.TEXT_COL[0], '#ffffff'), text='Upload',
                                    font=(settings.PRIMARY_FAMILY, 20), bg_color=settings.RECENTLY_PLAYED_COL,
                                    width=250, corner_radius=0, fg_color=settings.RECENTLY_PLAYED_COL,
                                    command=lambda: controller.show_frame(UploadFrame))

        self.upload.grid(row=3, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.settings = ctk.CTkButton(self, text_color=(settings.TEXT_COL[0], '#ffffff'), text='Settings',
                                      font=(settings.PRIMARY_FAMILY, 20), bg_color=settings.RECENTLY_PLAYED_COL,
                                      width=250, corner_radius=0, fg_color=settings.RECENTLY_PLAYED_COL,
                                      command=lambda: controller.show_frame(SettingsFrame))

        self.settings.grid(row=4, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.profile = ctk.CTkButton(self, text_color=(settings.TEXT_COL[0], '#ffffff'), text='Profile',
                                     font=(settings.PRIMARY_FAMILY, 20), bg_color=settings.RECENTLY_PLAYED_COL,
                                     width=250, corner_radius=0, fg_color=settings.RECENTLY_PLAYED_COL,
                                     command=lambda: controller.show_frame(ProfileFrame))

        self.profile.grid(row=5, column=0)