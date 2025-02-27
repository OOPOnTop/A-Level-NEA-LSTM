import customtkinter as ctk
import re
from GUI import gui_settings as settings
from Main_frames import MainFrames
import tkinter.messagebox
from Settings import SettingsFrame

ROWS = 4
COLUMNS = 2

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.configure(fg_color=settings.BG_COL)
        self.configure(bg_color=settings.BG_COL)

        self.show = True

        self.controller = controller

        self.tries = 0

        for i in range(ROWS):
            self.rowconfigure(i, weight=0)
        for i in range(COLUMNS):
            self.columnconfigure(i, weight=0)

        self.title_lable = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL, corner_radius=15,
                                        width=200, bg_color='transparent', text='Login Page',
                                        fg_color=settings.ACTIVE_BUTTON_COL, font=(settings.PRIMARY_FAMILY, 28, 'bold'))

        self.title_lable.grid(row=0, column=0, columnspan=3, pady=10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.email_entry = ctk.CTkEntry(self, fg_color='transparent', placeholder_text='email', placeholder_text_color=
                                        settings.NO_BG_TEXT_COL, width=300, font=(settings.PRIMARY_FAMILY, 24, 'bold'))

        self.email_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.password_entry = ctk.CTkEntry(self, fg_color='transparent', placeholder_text='password',
                                           placeholder_text_color=settings.NO_BG_TEXT_COL,
                                           font=(settings.PRIMARY_FAMILY, 24, 'bold'), show='*',
                                           text_color=settings.NO_BG_TEXT_COL, width=300)

        self.password_entry.grid(row=2, column=0, columnspan=2, padx=10)

        self.show_password_button = ctk.CTkButton(self, text_color=settings.NO_BG_TEXT_COL, text='Show',
                                                  font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                                  hover_color=settings.ACTIVE_BUTTON_COL, command=self.show_password)

        self.show_password_button.grid(row=2, column=2)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.login = ctk.CTkButton(self, text='Continue', text_color=settings.NO_BG_TEXT_COL,
                                   font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                   hover_color=settings.ACTIVE_BUTTON_COL, command=self.login_continue)

        self.login.grid(row=3, column=0, pady=10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.sign_up = ctk.CTkButton(self, text_color=settings.NO_BG_TEXT_COL, text='Sign Up',
                                     font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                     hover_color=settings.ACTIVE_BUTTON_COL, command=self.sign_up)

        self.sign_up.grid(row=3, column=2, pady=10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_password(self):
        if self.show:
            self.show = False
            self.show_password_button.configure(text='Hide')
            self.password_entry.configure(show='')
        else:
            self.show = True
            self.show_password_button.configure(text='Show')
            self.password_entry.configure(show='*')

    def login_continue(self):
        if self.tries >= 3:
            tkinter.messagebox.showerror(self,message='Too many failed attempts').show()
            self.controller.destroy()
        else:
            email_input = self.email_entry.get()
            try:
                res_email = self.controller.cur.execute("""SELECT email FROM user_info
                                                            WHERE email=?""", (email_input,)).fetchone()[0]
                password_input = self.password_entry.get()
                res_password = self.controller.cur.execute("""SELECT password FROM user_info
                                                            WHERE email=?""", (email_input,)).fetchone()[0]
            except:
                res_email = ''
                password_input = self.password_entry.get()
                res_password = ''

            if email_input == res_email:
                if password_input == res_password:
                    self.controller.user_id = self.controller.cur.execute("""SELECT infoID FROM user_info
                                                                            WHERE email?=""", (email_input,)).fetchone()[0]
                    self.controller.frames[MainFrames].update_user_id(self.controller.user_id)
                    self.controller.frames[MainFrames].frames[SettingsFrame].get_details()
                    self.controller.show_frame(MainFrames)
                    self.controller.geometry(settings.GEOMETRY)
                    self.controller.con.close()
                else:
                    tkinter.messagebox.Message(self, message="Invalid password \n Try again").show()
                    self.tries += 1
            else:
                tkinter.messagebox.Message(self, message="No account associated with this email").show()
                self.tries += 1

    def sign_up(self):
        self.controller.show_frame(SignUPScreen)
        self.controller.geometry('540x360')


class SignUPScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.configure(fg_color=settings.BG_COL)

        for i in range(8):
            self.rowconfigure(i, weight=0)
        for i in range(2):
            self.columnconfigure(i, weight=0)

        self.pword_show = False
        self.confirm_pword_show = False

        self.title_label = ctk.CTkLabel(self, text_color=settings.NO_BG_TEXT_COL,
                                        font=(settings.PRIMARY_FAMILY, 20, 'bold'), state="normal", fg_color='transparent',
                                        width=340)

        self.title_label.grid(row=0, column=0, columnspan=2, pady=5)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.name_input = ctk.CTkEntry(self, text_color=settings.NO_BG_TEXT_COL, font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                       state="normal", fg_color='transparent', placeholder_text='Name',
                                       placeholder_text_color=settings.NO_BG_TEXT_COL, width=340)

        self.name_input.grid(row=1, column=0, pady=10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.username_input = ctk.CTkEntry(self, text_color=settings.NO_BG_TEXT_COL, font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                           state="normal", fg_color='transparent', placeholder_text='Spotify Username',
                                           placeholder_text_color=settings.NO_BG_TEXT_COL, width=340)

        self.username_input.grid(row=2, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.email_input = ctk.CTkEntry(self, text_color=settings.NO_BG_TEXT_COL, font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                        state="normal", fg_color='transparent', placeholder_text='Email',
                                        placeholder_text_color=settings.NO_BG_TEXT_COL, width=340)

        self.email_input.grid(row=3, column=0, pady=10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.password_input = ctk.CTkEntry(self, text_color=settings.NO_BG_TEXT_COL, font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                           state="normal", fg_color='transparent', placeholder_text='Password',
                                           show="*", placeholder_text_color=settings.NO_BG_TEXT_COL, width=340)

        self.password_input.grid(row=4, column=0)

        self.show_pword_button = ctk.CTkButton(self, text_color=settings.NO_BG_TEXT_COL, text='Show', font=(settings.PRIMARY_FAMILY, 24, 'bold'),
                                               fg_color='transparent', hover_color=settings.ACTIVE_BUTTON_COL,
                                               command=self.show_pword)

        self.show_pword_button.grid(row=4, column=1, padx=10)

        self.password_details_label = ctk.CTkLabel(self, text="*Passwords must contain at least 1 letter, 1 number and 1"
                                                              " special character", text_color=settings.NO_BG_TEXT_COL,
                                                   bg_color=settings.BG_COL, font=(settings.PRIMARY_FAMILY, 11))

        self.password_details_label.grid(row=5, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.confirm_pword_input = ctk.CTkEntry(self, text_color=settings.NO_BG_TEXT_COL, font=(settings.PRIMARY_FAMILY, 20, 'bold'),
                                                state="normal", fg_color='transparent', placeholder_text='Confirm Password',
                                                show="*", placeholder_text_color=settings.NO_BG_TEXT_COL, width=340)

        self.confirm_pword_input.grid(row=6, column=0, pady=10, padx=10)

        self.show_confirm_pword_button = ctk.CTkButton(self, text_color=settings.NO_BG_TEXT_COL, text='Show',
                                                       font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                                       hover_color=settings.ACTIVE_BUTTON_COL,
                                                       command=self.show_confirm_pword)

        self.show_confirm_pword_button.grid(row=6, column=1, padx=10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.continue_button = ctk.CTkButton(self, text_color=settings.NO_BG_TEXT_COL, text='Continue',
                                             font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                             hover_color=settings.ACTIVE_BUTTON_COL, command=self.login)

        self.continue_button.grid(row=7, column=0)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.back_button = ctk.CTkButton(self, text_color=settings.NO_BG_TEXT_COL, text='Back',
                                             font=(settings.PRIMARY_FAMILY, 24, 'bold'), fg_color='transparent',
                                             hover_color=settings.ACTIVE_BUTTON_COL, command=self.back)

        self.back_button.grid(row=7, column=1)


    def show_pword(self):
        if self.pword_show:
            self.pword_show = not self.pword_show
            self.show_pword_button.configure(text='Hide')
            self.password_input.configure(show='')
        else:
            self.pword_show = not self.pword_show
            self.show_pword_button.configure(text='Show')
            self.password_input.configure(show='*')

    def show_confirm_pword(self):
        if self.confirm_pword_show:
            self.confirm_pword_show = not self.confirm_pword_show
            self.show_confirm_pword_button.configure(text='Show')
            self.confirm_pword_input.configure(show='*')
        else:
            self.confirm_pword_show = not self.confirm_pword_show
            self.show_confirm_pword_button.configure(text='Hide')
            self.confirm_pword_input.configure(show='')

    def back(self):
        self.name_input.delete(0, 'end')
        self.email_input.delete(0, 'end')
        self.password_input.delete(0, 'end')
        self.confirm_pword_input.delete(0, 'end')
        self.controller.show_frame(LoginScreen)
        self.controller.geometry('480x210')

    def login(self):
        new_name = self.name_input.get()
        username = self.username_input.get()
        new_email = self.email_input.get()
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        new_password = self.password_input.get()
        password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$"
        confirm_password = self.confirm_pword_input.get()
        if re.match(email_pattern, new_email):
            if new_password == confirm_password:
                if re.match(password_pattern, new_password):
                    self.controller.cur.execute("""INSERT INTO user_info(email, password, name, spotify_username) 
                                                VALUES(?,?,?,?)""",(new_email, new_password, new_name, username))
                    self.controller.con.commit()
                    self.controller.show_frame(LoginScreen)
                    self.controller.geometry('480x210')
                else:
                    tkinter.messagebox.Message(self, message="Password must contain at least 1 letter, 1 number and 1"
                                                             " special character").show()
            else:
                tkinter.messagebox.Message(self, message="Passwords do not match").show()
        else:
            tkinter.messagebox.Message(self, message="Invalid format for email").show()


