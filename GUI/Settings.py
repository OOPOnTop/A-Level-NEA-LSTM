import tkinter.messagebox
import customtkinter as ctk
from GUI import gui_settings as settings
from Home_screen_frame import HomeScreen
import re

ROWS = 5
COLUMNS = 3


class SettingsFrame(ctk.CTkFrame):
    """
        Frame that displays users profile details and allows changing of personal details and gui preferences, contains
        methods for changing these attributes during runtime and locally to a database
        """

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        # controller for frame switching
        self.controller = controller
        # button states
        self.name_index = True
        self.email_index = True
        self.password_index = False
        # initialise name email and password variables for fetching
        self.name = ''
        self.email = ''
        self.password = ''
        # user profile details
        self.user_id = ''
        self.details = []
        # light/dark mode state
        self.lg_state = True

        # setting colours
        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        # configure rows and columns
        for i in range(ROWS):
            self.rowconfigure(i, weight=0)
        for i in range(COLUMNS):
            self.columnconfigure(i, weight=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.settings_title = ctk.CTkLabel(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), corner_radius=35,
                                           fg_color=(settings.ACTIVE_BUTTON_COL[0], settings.RECENTLY_PLAYED_COL[1]),
                                           text='Settings', width=200,
                                           font=(settings.PRIMARY_FAMILY, 28, 'bold'))
        self.settings_title.grid(row=0, column=1, pady=30)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Name and change name bar
        self.name_bar = ctk.CTkLabel(self, text='Name', text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), bg_color=settings.BG_COL,
                                     font=(settings.PRIMARY_FAMILY, 24, 'bold'))
        self.name_bar.grid(row=1, column=0, padx=30)

        self.show_name = ctk.CTkEntry(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                      font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                      state="normal", fg_color='transparent',
                                      placeholder_text_color=settings.NO_BG_TEXT_COL, width=300)
        self.show_name.configure(state="normal")
        self.show_name.grid(row=1, column=1)

        self.change_name = ctk.CTkButton(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), text='Change Name',
                                         font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                         hover_color=settings.ACTIVE_BUTTON_COL,
                                         command=self.save_name_change)
        self.change_name.grid(row=1, column=2, columnspan=2)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # email and change email bar
        self.email_bar = ctk.CTkLabel(self, text='Email', text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                      bg_color=settings.BG_COL,
                                      font=(settings.PRIMARY_FAMILY, 24, 'bold'))
        self.email_bar.grid(row=2, column=0, padx=30, pady=30)

        self.show_email = ctk.CTkEntry(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                       font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                       state="normal", fg_color='transparent',
                                       placeholder_text_color=settings.NO_BG_TEXT_COL, width=300)
        self.show_email.configure(state="normal")
        self.show_email.grid(row=2, column=1, pady=30)

        self.change_email = ctk.CTkButton(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), text='Change email',
                                          font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                          hover_color=settings.ACTIVE_BUTTON_COL,
                                          command=self.save_email_change)
        self.change_email.grid(row=2, column=2, columnspan=2)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # password and change password bar
        self.pword_bar = ctk.CTkLabel(self, text='pword', text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                      bg_color=settings.BG_COL,
                                      font=(settings.PRIMARY_FAMILY, 24, 'bold'))
        self.pword_bar.grid(row=3, column=0, padx=30)

        self.show_pword = ctk.CTkEntry(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                       font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                       state="normal", fg_color='transparent',
                                       placeholder_text_color=settings.NO_BG_TEXT_COL, width=300, show='*')
        self.show_pword.configure(state="normal")
        self.show_pword.grid(row=3, column=1)

        self.show_pword_button = ctk.CTkButton(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), text='Show',
                                               font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                               hover_color=settings.ACTIVE_BUTTON_COL,
                                               command=self.allow_pword_change)
        self.show_pword_button.grid(row=3, column=2)

        self.confirm_pword_change = ctk.CTkButton(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"), text='Save',
                                                  font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                                  hover_color=settings.ACTIVE_BUTTON_COL,
                                                  command=self.save_pword_change)
        self.confirm_pword_change.grid(row=3, column=3)

        self.password_details_label = ctk.CTkLabel(self, text='*Passwords must contain at least 1 letter, 1 number and '
                                                              '1 special character',
                                                   text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                                   bg_color=settings.BG_COL,
                                                   font=(settings.PRIMARY_FAMILY, 11))
        self.password_details_label.grid(row=4, column=1, columnspan=1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # set light dark mode
        self.appearance_mode_label = ctk.CTkLabel(self, text='Appearance Mode',
                                                  text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                                  bg_color=settings.BG_COL, font=(settings.PRIMARY_FAMILY, 24, 'bold'))
        self.appearance_mode_label.grid(row=5, column=0, padx=30, pady=30)

        self.appearance_mode_button = ctk.CTkButton(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                                    text='Light/Dark',
                                                    font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                                    hover_color=settings.ACTIVE_BUTTON_COL,
                                                    command=self.change_appearance)
        self.appearance_mode_button.grid(row=5, column=2, columnspan=2, padx=30, pady=30)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Delete Account
        self.delete_account = ctk.CTkButton(self, text_color='#d41f00', text='Delete Account',
                                            font=(settings.PRIMARY_FAMILY, 19, 'bold'),
                                            fg_color='transparent',
                                            hover_color=settings.ACTIVE_BUTTON_COL,
                                            command=self.delete_account)
        self.delete_account.grid(row=6, column=0, columnspan=1)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Save and continue
        self.save_details_button = ctk.CTkButton(self, text_color=(settings.NO_BG_TEXT_COL[0], "#ffffff"),
                                                 text='Continue',
                                                 font=(settings.PRIMARY_FAMILY, 24, 'bold'),
                                                 fg_color='transparent',
                                                 hover_color=settings.ACTIVE_BUTTON_COL,
                                                 command=lambda: controller.show_frame(HomeScreen))
        self.save_details_button.grid(row=6, column=1, columnspan=2)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # functions
    def save_name_change(self):
        """
        Function that enables and disables editing of entry box for name as well as changing button text to match
        current state
        :return:
        """
        if self.name_index:
            self.name_index = False
            self.show_name.configure(state="normal")
            self.change_name.configure(text='Save')
            self.show_name.focus_set()

        else:
            self.name_index = True
            self.show_name.configure(state="disabled")
            self.change_name.configure(text='Change Name')
            self.name = self.show_name.get()
            self.controller.cur.execute("""UPDATE user_info
                                                        SET name=?
                                                        WHERE infoID=?""", (self.name, self.user_id,))
            self.controller.con.commit()

    def save_email_change(self):
        """
        Function that enables and disables editing of entry box for email as well as changing button text to match
        current state and performing local validation for email format
        :return:
        """
        if self.email_index:
            self.email_index = False
            self.show_email.configure(state="normal")
            self.show_email.focus_set()
            self.change_email.configure(text='Save')

        else:
            email = self.show_email.get()
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if re.match(pattern, email):
                self.email_index = False
                self.show_email.configure(state="disabled")
                self.email = email
                self.controller.cur.execute("""UPDATE user_info
                                            SET email=?
                                            WHERE infoID=?""", (self.email, self.user_id,))
                self.controller.con.commit()
                self.email_index = True
                self.show_email.configure(state="disabled")
                self.change_email.configure(text='Change email')
            else:
                tkinter.messagebox.Message(self, message='Invalid format for email address').show()

    def allow_pword_change(self):
        """
        Function that enables and disables editing of entry box for password as well as changing button text to match
        current state
        :return:
        """
        self.password_index = not self.password_index
        if self.password_index:
            self.show_pword.configure(show='')
            self.show_pword_button.configure(text='Hide')
            self.show_pword.configure(state='normal')
            self.show_pword.focus_set()
        else:
            self.show_pword.configure(show='*')
            self.show_pword_button.configure(text='Show')
            self.show_pword.configure(state='disabled')

    def save_pword_change(self):
        """
        Performs local validation for password format#
        Current requirements:
            - min 8 chars
            - min 1 letter
            - min 1 num
            - min 1 special char
        :return:
        """
        password = self.show_pword.get()
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if re.match(pattern, password):
            answer = tkinter.messagebox.askyesno(title='Confirm Password', message='Confirm Password Change')
            if answer:
                self.password_index = False
                self.show_pword.configure(state="disabled")
                self.show_pword.configure(show='*')
                self.password = password
                self.controller.cur.execute("""UPDATE user_info
                                                            SET password=?
                                                            WHERE infoID=?""", (self.password, self.user_id,))
                self.controller.con.commit()
            else:
                pass
        else:
            tkinter.messagebox.Message(self, message='Invalid format for password').show()
            self.show_pword.delete(0, 'end')
            self.show_pword.insert(0, self.password)
            self.show_pword.focus_set()

    def change_appearance(self):
        """
        Changes button state to match theming, changes colour scheme between light and dark mode
        :return:
        """
        self.lg_state = not self.lg_state
        if self.lg_state:
            ctk.set_appearance_mode('Light')
        else:
            ctk.set_appearance_mode('Dark')

    def delete_account(self):
        """
        Gives user choice to delete account and the data associated with it from the database
        :return:
        """
        answer = tkinter.messagebox.askyesno(title='Confirm Delete', message='Are you sure you would like to delete '
                                                                             'your account?')
        if answer:
            self.controller.cur.execute("""DELETE FROM user_info WHERE infoID=?""", (self.user_id,))
            self.controller.con.commit()
            self.controller.con.close()
            self.controller.controller.destroy()
        else:
            pass

    def get_details(self):
        """
        Method to update users details across the application during runtime so SQL statements are correct at all
        times to avoid errors
        :return:
        """
        self.user_id = self.controller.user_id
        self.details = self.controller.cur.execute("""SELECT name, email, password FROM user_info
                                                        WHERE infoID=? """, (self.user_id,)).fetchone()[0:3]
        self.name = self.details[0]
        self.show_name.insert(0, self.name)
        self.show_name.configure(state="disabled")

        self.email = self.details[1]
        self.show_email.insert(0, self.email)
        self.show_email.configure(state="disabled")

        self.password = self.details[2]
        self.show_pword.insert(0, self.password)
        self.show_pword.configure(state="disabled")
