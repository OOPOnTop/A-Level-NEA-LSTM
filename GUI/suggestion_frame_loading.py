import gui_settings as settings
import customtkinter as ctk
from suggestion_frame_display_frame import SuggestionDisplayContainer


class SuggestionLoading(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.configure(width=800)
        self.configure(height=420)
        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

        self.Suggestion_frame = None

        self.ideal_songs = None

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.suggestion_title = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=30,
                                             fg_color=settings.ACTIVE_BUTTON_COL, text="Suggestions", width=200,
                                             font=(settings.PRIMARY_FAMILY, 32, 'bold'))

        self.suggestion_title.grid(row=0, column=1, pady=30)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.progress_bar = ctk.CTkProgressBar(self, determinate_speed=0.6, width=300,
                                               height=20, corner_radius=5)

        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=1, pady=10, padx=10)

        self.button = ctk.CTkButton(self, text="Generate Songs", font=(settings.PRIMARY_FAMILY, 28, 'bold'),
                                    width=200, height=50, command=self.clicked)

        self.button.grid(row=2, column=1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def clicked(self):
        self.progress_bar.start()
        self.ideal_songs = self.controller.generate_songs()
        self.progress_bar.after(3000, func=self.finish_clicked)

    def finish_clicked(self):
        self.controller.loading_frame.destroy()
        self.Suggestion_frame = SuggestionDisplayContainer(self.parent, self.controller, self.ideal_songs)
        self.Suggestion_frame.fill()
        self.Suggestion_frame.grid(row=0, column=0, padx=200, pady=125, sticky="nsew")
