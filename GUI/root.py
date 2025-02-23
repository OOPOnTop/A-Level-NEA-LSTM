import customtkinter as ctk
from GUI import gui_settings as settings
from Login_Page import LoginScreen, SignUPScreen
from Main_frames import MainFrames
import sqlite3
from AI_models import LSTM
from Spotify_API_query import APICalls

class MusicApp(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.iconbitmap(self, default="icon.ico")
        self.geometry('480x210')
        self.title(settings.ROOT_TITLE)

        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)

        self.con = sqlite3.connect('Users.db')
        self.cur = self.con.cursor()
        self.user_id = ''

        self.spotify_username = self.cur.execute("""SELECT spotify_username FROM user_info WHERE infoID=?""",
                                                 (self.user_id,)).fetchone()
        self.API_caller = APICalls(self.spotify_username)

        self.features = self.API_caller.recetly_played_song_features()
        self.train_features = self.format_features()

        self.network = LSTM(self.train_features)
        self.ideal_features = []

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=1)

        self.protocol('WM_DELETE_WINDOW')

        self.frames = {}
        for F in (MainFrames, SignUPScreen, LoginScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.login = LoginScreen(container, self)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

    def format_features(self):
        features = []
        for i in self.features:
            song_features = []
            feature_dict = i[1]
            for key in feature_dict.keys():
                if key == 'Tempo':
                    song_features.append([feature_dict[key]/1000])
                elif key == 'Duration':
                    song_features.append([feature_dict[key]/1000000])
                else:
                    song_features.append([feature_dict[key]])
            features.append(song_features)
        return features

app = MusicApp()
app.resizable(False, False)
app.mainloop()