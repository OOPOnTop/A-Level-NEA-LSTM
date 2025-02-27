from __future__ import annotations
import customtkinter as ctk
from GUI import gui_settings as settings
from PIL import Image
import textwrap


class SearchBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.query = self.parent.controller.API_caller

        self.configure(fg_color=settings.RECENTLY_PLAYED_COL)
        self.configure(width=800)
        self.configure(height=400)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)

        self.results = []

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.search_field = ctk.CTkEntry(self, border_color=(settings.BORDER_COL, "#ffffff"),
                                         placeholder_text='Search', bg_color=settings.BG_COL,
                                         width=settings.SEARCH_BAR_WIDTH, height=40, border_width=2,
                                         text_color=(settings.BORDER_COL, "#ffffff"))

        self.search_field.grid(row=0, column=0)

        self.search_icon = ctk.CTkImage(Image.open('/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/GUI/search.png'), size=(32, 32))

        self.search_button = ctk.CTkButton(self, image=self.search_icon, bg_color=settings.BG_COL,
                                           border_width=0, hover_color=settings.ACTIVE_BUTTON_COL,
                                           text='', width=32, command=self.search)

        self.search_button.grid(row=0, column=1)

    def search(self):
        q = self.search_field.get()
        if q:
            self.parent.frames["search-results"].clear_frames()
            self.results = self.query.search_bar_search(q=q)
            self.parent.frames["search-results"].fill_frame()
            self.parent.show_frame("search-results")

        else:
            pass


class SearchResults(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.controller = controller
        self.frame = SearchResultsScrollable(self, self.controller)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20)

        self.configure(fg_color=settings.BG_COL)

    def clear_frame(self):
        self.frame.destroy()

    def fill_frame(self):
        self.frame = SearchResultsScrollable(self, self.controller)
        self.frame.search_results()
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20)


class SearchResultsScrollable(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.search_artist_title = None
        self.search_song_title = None
        self.artists = []
        self.songs = []
        self.parent = parent
        self.controller = controller
        self.query = self.controller.controller.API_caller

        self.configure(fg_color=settings.RECENTLY_PLAYED_COL)

        self.configure(label_text='Results', label_font=(settings.PRIMARY_FAMILY, 22, 'bold'),
                       label_fg_color=settings.BG_COL, label_text_color=settings.NO_BG_TEXT_COL, label_anchor='center')

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        for i in range(len(self.controller.search_bar.results) + 2):
            self.rowconfigure(i, weight=0)

    def search_results(self):
        self.search_song_title = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=35,
                                              fg_color=settings.BG_COL, text='Song',
                                              width=225, font=(settings.PRIMARY_FAMILY, 26, 'bold'))

        self.search_song_title.grid(row=0, column=0, columnspan=1, padx=28, sticky='nsew')

        self.search_artist_title = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=35,
                                                fg_color=settings.BG_COL, text='Artist',
                                                width=225, font=(settings.PRIMARY_FAMILY, 26, 'bold'))

        self.search_artist_title.grid(row=0, column=1, columnspan=1, padx=28, sticky='nsew')

        self.songs = []
        self.artists = []

        for i, item in enumerate(self.controller.search_bar_results):
            song = ctk.CTkLabel(self, text_color=(settings.NO_BG_TEXT_COL[0], settings.BG_COL[1]), corner_radius=35,
                                text=textwrap.fill(item[1], width=35),
                                width=200, font=(settings.PRIMARY_FAMILY, 18, 'bold'))

            self.songs.append(song)
            song.grid(row=i + 1, column=0, padx=20, pady=3)

            artist = ctk.CTkLabel(self, text_color=(settings.NO_BG_TEXT_COL[0], settings.BG_COL[1]), corner_radius=35,
                                text=textwrap.fill(item[3], width=35),
                                width=200, font=(settings.PRIMARY_FAMILY, 18, 'bold'))

            self.songs.append(artist)
            artist.grid(row=i + 1, column=1, padx=20, pady=3)
