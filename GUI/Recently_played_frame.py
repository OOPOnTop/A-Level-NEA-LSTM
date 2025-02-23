import customtkinter as ctk
import gui_settings as settings
import textwrap


class RecentlyPlayed(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame = RecentlyPlayedScrollable(self, controller)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20)

        self.configure(fg_color=settings.BG_COL)
        self.configure(width=700)
        self.configure(height=320)


class RecentlyPlayedScrollable(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller
        self.query = self.controller.controller.API_caller

        self.configure(width=700)
        self.configure(height=320)
        self.configure(fg_color=settings.RECENTLY_PLAYED_COL)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        for i in range(51):
            self.rowconfigure(i, weight=0)

        self.configure(label_text="Recently Played", label_font=(settings.PRIMARY_FAMILY, 22, 'bold'),
                       label_fg_color=settings.BG_COL, label_text_color=(settings.TEXT_COL[0], "#ffffff"),
                       label_anchor='center')

        self.recently_played_songs = self.query.played_songs

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.song_label = ctk.CTkLabel(self, text="Song name", text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                      font=(settings.PRIMARY_FAMILY, 18, 'bold'), width=200, corner_radius=35,
                                       fg_color=settings.BG_COL,)

        self.song_label.grid(row=0, column=0, padx=55, sticky='w')

        self.artist_label = ctk.CTkLabel(self, text="Artist", text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                         font=(settings.PRIMARY_FAMILY, 18, 'bold'), width=200, corner_radius=35,
                                         fg_color=settings.BG_COL)

        self.artist_label.grid(row=0, column=1, padx=55, sticky='e')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.songs = []
        self.artists = []
        for i in range(50):
            song = ctk.CTkLabel(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), corner_radius=35,
                                text = textwrap.fill(self.recently_played_songs[i][0], width=25),
                                width=200, font=(settings.PRIMARY_FAMILY, 18, 'bold'), fg_color=settings.BG_COL)

            self.songs.append(song)
            song.grid(row=i+1, column=0, padx=60, pady=3, sticky='w')

            artist = ctk.CTkLabel(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), corner_radius=35,
                                  text = textwrap.fill(self.recently_played_songs[i][1], width=25),
                                  width=200, font=(settings.PRIMARY_FAMILY, 18, 'bold'))

            self.artists.append(artist)
            artist.grid(row=i+1, column=1, padx=60, pady=3, sticky='e')
