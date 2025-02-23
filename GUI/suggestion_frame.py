import gui_settings as settings
import customtkinter as ctk
from suggestion_frame_loading import SuggestionLoading


class SuggestionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.API_caller = self.controller.API_caller
        self.network = self.controller.network
        self.train_features = self.controller.train_features
        self.ideal_features = []
        self.ideal_songs = []

        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.loading_frame = SuggestionLoading(self, self)
        self.loading_frame.grid(row=0, column=0, padx=200, pady=125, sticky="nsew")

    def generate_songs(self):
        self.ideal_features = self.network.get_prediction()
        self.ideal_songs = self.API_caller.search_by_features(self.ideal_features, limit=25)
        return self.ideal_songs