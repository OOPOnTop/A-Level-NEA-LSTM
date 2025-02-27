import customtkinter as ctk
import gui_settings as settings
from PIL import Image

ROWS = 4
COLUMNS = 1


class UploadFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        for i in range(ROWS):
            self.rowconfigure(i, weight=0)
        for i in range(COLUMNS):
            self.columnconfigure(i, weight=0)

        self.file = []

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.upload_title = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=35,
                                         fg_color=settings.ACTIVE_BUTTON_COL, text="Upload", width=200,
                                         font=(settings.PRIMARY_FAMILY, 28, 'bold'))

        self.upload_title.grid(row=0, column=0, columnspan=2, pady=30)

        self.image = ctk.CTkImage(Image.open('/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/GUI/privacy-step3.png'), size=(390, 450))
        self.explain_box_image = ctk.CTkLabel(self, text='', image = self.image)
        self.explain_box_image.grid(row=1, column=1, rowspan=4)

        self.explain_box = ctk.CTkLabel(self, text='Navigate to your Spotify profile and select privacy settings then '
                                                   'select download extended streaming history. \n\n'
                                                   'Once the data has arrived in an email, download the zip file and '
                                                   'extract all, then upload any files in format StreamingHistory#.json'
                                                   ' using the upload data button on this page.',
                                        wraplength=475, justify='left', font=(settings.PRIMARY_FAMILY, 18),
                                        text_color=settings.NO_BG_TEXT_COL)

        self.explain_box.grid(row=1, column=0, padx=20)

        self.data_image = ctk.CTkImage(Image.open('/Users/charlie/PycharmProjects/A-Level-NEA-LSTM/GUI/data_example.png'), size=(525, 155))
        self.data_image_box = ctk.CTkLabel(self, text='', image=self.data_image)
        self.data_image_box.grid(row=2, column=0, padx=10)

        self.filler_text = ctk.CTkLabel(self, text='To ass in a future release', fg_color=settings.ACTIVE_BUTTON_COL,
                                        text_color=settings.NO_BG_TEXT_COL, font=(settings.PRIMARY_FAMILY, 24, 'bold'),
                                        corner_radius=10)

        self.filler_text.grid(row=3, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def validate_files(self):
        pass

    def file_select_to_recently_played(self):
        pass
