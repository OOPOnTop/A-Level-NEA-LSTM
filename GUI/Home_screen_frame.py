import customtkinter as ctk
from GUI import gui_settings as settings
from Recently_played_frame import RecentlyPlayed
from blank_space import BlankSpace
from search import SearchBar, SearchResults


class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color=settings.BG_COL)
        self.controller = controller
        self.API_caller = self.controller.API_caller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        self.search_bar = SearchBar(self)
        self.search_bar.grid(row=0, column=0, columnspan=3)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.blank_space = BlankSpace(self, settings.SCROLLABLE_WIDTH + 50, settings.BG_COL,
                                      height=settings.RECENTLY_PLAYED_BLANK_SPACE)

        self.blank_space.grid(row=2, column=0, columnspan=2)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.frames = {}
        frame_setup = {
            "search-results": SearchResults,
            "recently-played": RecentlyPlayed
        }

        for name, frame in frame_setup.items():
            new_frame = frame(self, self)
            self.frames[name] = new_frame
            new_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()
