import customtkinter as ctk
from GUI import gui_settings as settings
from Home_screen_frame import HomeScreen
from profile_page import ProfileFrame
from side_bar import SideBar
from Settings import SettingsFrame
from upload_frame import UploadFrame
from suggestion_frame import SuggestionFrame
import sqlite3


class MainFrames(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        self.con = sqlite3.connect('Users.db')
        self.cur = self.con.cursor()
        self.user_id = self.controller.user_id
        self.spotify_username = self.controller.spotify_username

        self.API_caller = self.controller.API_caller

        self.network = self.controller.network
        self.train_features = self.controller.train_features

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=1)

        self.frames = {}
        for F in (HomeScreen, ProfileFrame, SettingsFrame, UploadFrame, SuggestionFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=1, sticky="nsew")

        self.show_frame(HomeScreen)

        self.menu_side_bar = SideBar(container, self)
        self.menu_side_bar.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, controller):
        frame = self.frames[controller]
        if controller == HomeScreen:
            frame.show_frame("recently-played")

        frame.tkraise()

    def update_user_id(self, id):
        self.user_id = id
