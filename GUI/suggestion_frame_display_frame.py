from cProfile import label

import gui_settings as settings
import customtkinter as ctk
import textwrap


class SuggestionDisplayContainer(ctk.CTkFrame):
    def __init__(self, parent, controller, ideal_songs):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.configure(bg_color=settings.BG_COL)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.info = None
        self.ideal_songs = ideal_songs

    def fill(self):
        self.info = SuggestionDisplay(self.parent, self.controller, self.ideal_songs)
        self.info.grid(row=0, column=0, padx=80, pady=70)


class SuggestionDisplay(ctk.CTkFrame):
    def __init__(self, parent, controller, ideal_songs):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.configure(width=800)
        self.configure(height=405)

        self.configure(label_text="Suggestions", label_font=(settings.PRIMARY_FAMILY, 28, 'bold'),
                       label_fg_color=settings.BG_COL, label_text_color=settings.NO_BG_TEXT_COL, label_anchor='center')

        self.configure(bg_color=settings.BG_COL)
        self.configure(fg_color=settings.RECENTLY_PLAYED_COL)

        for i in range(26):
            self.rowconfigure(i, weight=0)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        self.ideal_songs = ideal_songs

        self.songs = []
        self.artists = []

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.song_label = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=35,
                                       fg_color=settings.BG_COL, text='Song Name',
                                       width=180, font=(settings.PRIMARY_FAMILY, 26, 'bold'))

        self.song_label.grid(row=1, column=0, padx=15, sticky='nsew')

        self.artist_label = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=35,
                                       fg_color=settings.BG_COL, text='Artist',
                                       width=180, font=(settings.PRIMARY_FAMILY, 26, 'bold'))

        self.artist_label.grid(row=1, column=1, padx=15, sticky='nsew')

        for i in range(len(self.ideal_songs)):
            song = ctk.CTkLabel(self, text_color=(settings.NO_BG_TEXT_COL[0], settings.BG_COL[1]), corner_radius=35,
                                tetx=textwrap.fill(self.ideal_songs[i][1], width=40),
                                width=200, font=(settings.PRIMARY_FAMILY, 22, 'bold'))

            self.songs.append(song)
            song.grid(row=i+2, column=0, padx=15, pady=3)

            artist = ctk.CTkLabel(self, text_color=(settings.NO_BG_TEXT_COL[0], settings.BG_COL[1]), corner_radius=35,
                                tetx=textwrap.fill(self.ideal_songs[i][3], width=40),
                                width=200, font=(settings.PRIMARY_FAMILY, 22, 'bold'))

            self.artists.append(artist)
            artist.grid(row=i + 2, column=1, padx=15, pady=3)
