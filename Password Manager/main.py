# =============================================================================
#                                Libraries
# =============================================================================
import tkinter
from tkinter import *
from tkinter import messagebox
import os
import json
import smtplib
from email.message import EmailMessage
from typing import Dict, Union

# =============================================================================
#                             Global Variables
# =============================================================================
data = {}
icon = os.environ.get("ICON")
passwords_file_path = os.environ.get("FILE_PATH")
python_email = os.environ.get("PYTHON_MAIL")
email_password = os.environ.get("EMAIL_PASSWORD")


# =============================================================================
#                                Functions
# =============================================================================
def send_email() -> None:
    """
    The function takes from data user_email and log_in_psw. Then send email with password to user mail.

    :return: None
    """
    global python_email
    global email_password

    message = EmailMessage()
    message['Subject'] = 'Password Reminder'
    message['From'] = 'Password Manager'
    message['To'] = data['user_email']
    message.set_content('''Hello, I am creator of password manager.
Here is your password: {}
Have a nice day! - MB '''.format(data['log_in_psw']))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(python_email, email_password)
            smtp.send_message(message)
            smtp.close()
            messagebox.showinfo(title='Success', message=f'Email sent to {data["user_email"]} !')
    except Exception as e:
        messagebox.showinfo(title='Error', message=f'{e}')


def save_data(path: str, data_arg: Dict) -> None:
    """
    The function saves existing data

    :param path: str
    :param data_arg: Dict
    :return: None
    """
    try:
        with open(path, 'w') as f:
            data_json = json.dumps(data_arg, separators=(',', ':'))
            encrypted_data = encrypt_string(data_json)
            json.dump(encrypted_data, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror(title="Error", message=f"Cannot save the data file!")


def load_data() -> None:
    """
    The function loads existing data. If data doesn't exist it create variable data which is empty dictionary

    :return: None
    """
    global data
    try:
        with open(passwords_file_path, 'r') as f:
            encrypted_data = json.load(f)
            data = json.loads(decrypt_string(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    else:
        print("File opened successfully")


# Check password - window
def open_password_checking_window(button_name: str) -> None:
    """
    The function opens password checking window and user can entry password

    :param button_name: str
    :return: None
    """
    check_password_window = Toplevel()
    check_password_window.iconbitmap(icon)
    check_password_window.geometry('220x120')
    check_password_window.title(f'{button_name}')

    change_password_label = Label(check_password_window, text='Entry your password')
    change_password_label.pack()

    check_password_input = Entry(check_password_window)
    check_password_input.pack()

    change_password_button = Button(check_password_window, text='Check password',
                                    command=lambda: check_password(check_password_input, check_password_window))
    change_password_button.pack()


def check_password(log_in_input_arg: tkinter.Entry, window: tkinter.Toplevel) -> None:
    """
    The function checks entered parameter log_in_input_arg and then decide whether open next window or show error

    :param log_in_input_arg: tkinter.Entry
    :param window: tkinter.Toplevel
    :return: None
    """

    log_in_input = log_in_input_arg.get()

    if not log_in_input == data['log_in_psw']:
        messagebox.showwarning(title='Wrong password', message='Wrong password, access denied')
        password_check_window.destroy()
    else:
        messagebox.showinfo(title='Success', message='Correct password')
        # If we successfully logged in buttons will be enabled
        if window.title() == 'Log in':
            enable_all_buttons()
        # If we want to change password - first we check if entered password is correct,
        # then open window where user can change the password
        elif window.title() == 'Change Password':
            open_change_password_window()
        # If we want to delete data - we need to check password first
        elif window.title() == 'Clear Database':
            clear_database_popup()
        elif window.title() == 'Change Email':
            open_change_email_window()
    window.destroy()


def disable_all_buttons() -> None:
    """
    The function disable all buttons on root

    :return: None
    """
    b_choice_1.config(state="disabled")
    b_choice_2.config(state="disabled")
    b_choice_3.config(state="disabled")
    b_choice_4.config(state="disabled")
    b_choice_5.config(state="disabled")
    b_choice_6.config(state="disabled")
    b_choice_7.config(state="disabled")
    b_choice_8.config(state="disabled")
    b_choice_9.config(state="disabled")
    b_choice_10.config(state="disabled")


def enable_all_buttons() -> None:
    """
    The unction enable all buttons except "Login" button on root

    :return: None
    """
    b_choice_0.config(state="disabled")
    b_choice_1.config(state="normal")
    b_choice_2.config(state="normal")
    b_choice_3.config(state="normal")
    b_choice_4.config(state="normal")
    b_choice_5.config(state="normal")
    b_choice_6.config(state="normal")
    b_choice_7.config(state="normal")
    b_choice_8.config(state="normal")
    b_choice_9.config(state="normal")
    b_choice_10.config(state="normal")


# Encrypt the given string - letter shift is variable: number
def encrypt_string(string: str, number: int = 225) -> Union[str, None]:
    """
    The function take a string and then encrypt it and return encrypted string

    :param string: str
    :param number: int
    :return: Union[str, None]
    """
    encrypted_string = ''
    for word in string:
        for letter in word:
            shift = (ord(letter) - ord("!") + number) % 94
            encrypted_string += chr(shift + ord('!'))

    if isinstance(string, str) and isinstance(number, int):
        return encrypted_string
    else:
        return None


# Decrypt the given string - letter shift is variable: number
def decrypt_string(string: str, number: int = 225) -> Union[str, None]:
    """
    Function take an encrypted string and then decrypt it and return decrypted string

    :param string: str
    :param number: int
    :return: Union[str, None]
    """
    decrypted_string = ''
    for letter in string:
        shift = (ord(letter) - ord('!') - number) % 94
        decrypted_string += chr(shift + ord('!'))

    if isinstance(string, str) and isinstance(number, int):
        return decrypted_string
    else:
        return None


# =============================================================================
#                   DECIDE WHICH WINDOW SHOULD OPEN- Config
# =============================================================================
# If user already have set password open login window else open password_to_set_window
def decide_set_or_entry() -> None:
    """
    The function decides which function to open next. If 'data['log_in_psw']' and 'data['user_email']' are present,
    it opens 'login_window()'. If not, it opens 'open_set_password_window()'

    :return: None
    """
    global data
    global password_check_window
    try:
        if data['log_in_psw'] and data['user_email']:
            password_check_window = Toplevel(root)
            password_check_window.iconbitmap(icon)
            password_check_window.geometry('220x130')
            password_check_window.title('Log in')
            login_window(password_check_window)
    except KeyError:
        password_to_set_window = Toplevel(root)
        password_to_set_window.iconbitmap(icon)
        password_to_set_window.geometry('300x120')
        password_to_set_window.title('Set a password')
        open_set_password_window(password_to_set_window)


# =============================================================================
#                         LOGIN WINDOW - Config
# =============================================================================
def login_window(password_check_window_arg: tkinter.Toplevel) -> None:
    """
    The function opens login window in which user can log in to password manager also they can click
    forgot_password_button and password will be sent to given email

    :param password_check_window_arg: tkinter.Toplevel
    :return: None
    """
    log_in_label = Label(password_check_window_arg, text='Enter a password')
    log_in_label.pack()

    log_in_entry = Entry(password_check_window_arg, width=25)
    log_in_entry.pack()

    log_in_button = Button(password_check_window_arg, text='Log in',
                           command=lambda: check_password(log_in_entry, password_check_window_arg))
    log_in_button.pack()

    forgot_password_button = Button(password_check_window_arg, text='Forgot your password?',
                                    command=lambda: send_email())

    forgot_password_button.pack()


# =============================================================================
#                         PASSWORD SET WINDOW - Config
# =============================================================================
def open_set_password_window(password_set_window: tkinter.Toplevel) -> None:
    """
    The function opens window in which user enter password and email that they want to set

    :param password_set_window: tkinter.Toplevel
    :return: None
    """
    password_set_label = Label(password_set_window, text='Set a password')
    password_set_label.pack()

    password_set_input = Entry(password_set_window, width=40)
    password_set_input.pack()

    email_set_label = Label(password_set_window, text='Enter your email')
    email_set_label.pack()

    email_set_input = Entry(password_set_window, width=40)
    email_set_input.pack()

    password_set_button = Button(password_set_window, text='Set password',
                                 command=lambda: set_password(password_set_input, email_set_input,
                                                              password_set_window))
    password_set_button.pack()


# Write password and email into JSON file
def set_password(password_set_input_arg: tkinter.Entry, email_set_input_arg: tkinter.Entry,
                 window: tkinter.Toplevel) -> None:
    """
    The function takes entered parameters in open_set_password_window() function and then write them into .JSON file

    :param password_set_input_arg: tkinter.Entry
    :param email_set_input_arg: tkinter.Entry
    :param window: tkinter.Toplevel
    :return: None
    """
    global data
    password_set_input = password_set_input_arg.get()
    email_set_input = email_set_input_arg.get()

    if password_set_input == '' or email_set_input == '':
        messagebox.showerror(title='Error', message='Any field cannot be empty!')
    else:
        data['log_in_psw'] = password_set_input
        data['user_email'] = email_set_input
        # # Saving data immediately
        save_data(passwords_file_path, data)

        # Enable all buttons function
        enable_all_buttons()
    window.destroy()


# =============================================================================
#                         TOPLEVEL(root) - Config
# =============================================================================
#                    Change password (Option 1) - Config
# =============================================================================
# Change password - window after check password window
def open_change_password_window() -> None:
    """
    The function open window in which user enter new password and then open change_login_password() function

    :return: None
    """
    change_password_window_ac = Toplevel()
    change_password_window_ac.iconbitmap(icon)
    change_password_window_ac.geometry('220x120')
    change_password_window_ac.title('Change Password')

    change_password_window_ac_label = Label(change_password_window_ac, text='Entry new password')
    change_password_window_ac_label.pack()

    new_password_input = Entry(change_password_window_ac)
    new_password_input.pack()

    change_password_window_ac_button = Button(change_password_window_ac, text='Change password',
                                              command=lambda: change_login_password(new_password_input,
                                                                                    change_password_window_ac))
    change_password_window_ac_button.pack()


# Change login password - function
def change_login_password(new_password_arg: tkinter.Entry, window: tkinter.Toplevel) -> None:
    """
    The function takes entered parameter(new_password_arg) and then change existing password to new_password_arg

    :param new_password_arg: tkinter.Entry
    :param window: tkinter.Toplevel
    :return: None
    """
    global data
    new_password = new_password_arg.get()
    if new_password == '':
        messagebox.showwarning(title='Warning', message='New password cannot be empty!')
    else:
        data['log_in_psw'] = new_password
        messagebox.showinfo(title='Success', message='Password changed successfully')
        window.destroy()
        password_check_window.destroy()
        #  Saving new password to the file
        save_data(passwords_file_path, data)


# =============================================================================
#                    Change email (Option 2) - Config
# =============================================================================
# Change email - window config - button 2 root
def open_change_email_window() -> None:
    """
    The function open window in which user enter new email and then open change_email() function

    :return: None
    """
    change_email_window = Toplevel()
    change_email_window.iconbitmap(icon)
    change_email_window.geometry('330x120')
    change_email_window.title('Change Email')

    change_email_window_label = Label(change_email_window, text='Entry new email')
    change_email_window_label.pack()

    new_email_input = Entry(change_email_window, width=40)
    new_email_input.pack()

    change_password_window_ac_button = Button(change_email_window, text='Change email',
                                              command=lambda: change_email(new_email_input, change_email_window))
    change_password_window_ac_button.pack()


# Change email - function
def change_email(new_email_arg: tkinter.Entry, window: tkinter.Toplevel) -> None:
    """
    The function takes entered parameter(new_email_arg) and then change existing email to new_email_arg

    :param new_email_arg: tkinter.Entry
    :param window: tkinter.Toplevel
    :return: None
    """
    global data
    new_email = new_email_arg.get()
    if new_email == '':
        messagebox.showwarning(title='Warning', message='New email cannot be empty!')
    elif new_email.find('@') < 1:
        messagebox.showwarning(title='Warning', message='Wrong email format!')
    else:
        data['user_email'] = new_email
        messagebox.showinfo(title='Success', message='Email changed successfully')
        save_data(passwords_file_path, data)
        window.destroy()
        password_check_window.destroy()


# =============================================================================
#                     Adding new data (Option 3) - Config
# =============================================================================
# Data window - configuration - button 3 root
def open_new_data_window() -> None:
    """
    The function open window in which user input new data and then opens add_new_data_to_database function

    :return: None
    """
    new_data_window = Toplevel(root)
    new_data_window.iconbitmap(icon)
    new_data_window.geometry('300x180')
    new_data_window.title('Add New Data')

    site_label = Label(new_data_window, text='Enter a website or application name')
    site_label.pack()
    site_input = Entry(new_data_window, width=35)
    site_input.pack()

    login_label = Label(new_data_window, text='Enter a login')
    login_label.pack()
    login_input = Entry(new_data_window, width=35)
    login_input.pack()

    password_label = Label(new_data_window, text='Enter a password')
    password_label.pack()
    password_input = Entry(new_data_window, width=35)
    password_input.pack()

    get_data_button = Button(new_data_window, text='Save the data',
                             command=lambda: add_new_data_to_database(site_input, login_input, password_input,
                                                                      new_data_window),
                             pady=5)
    get_data_button.pack()

    # Adding new data to database
    def add_new_data_to_database(site_input_arg: tkinter.Entry, login_input_arg: tkinter.Entry,
                                 password_input_arg: tkinter.Entry, window: tkinter.Toplevel) -> None:
        """
        The function add taken parameters to database

        :param site_input_arg: tkinter.Entry
        :param login_input_arg: tkinter.Entry
        :param password_input_arg: tkinter.Entry
        :param window: tkinter.Toplevel
        :return: None
        """
        global data
        site = site_input_arg.get().lower()
        login = login_input_arg.get()
        password = password_input_arg.get()

        if site == '' or login == '' or password == '':
            messagebox.showwarning(title="Warning", message="Any field cannot be empty!")
        elif site not in data:
            data[site] = [{'login': login, 'password': password}]
            save_data(passwords_file_path, data)
        else:
            data[site].append({'login': login, 'password': password})
            save_data(passwords_file_path, data)
        window.destroy()


# =============================================================================
#                         DELETE DATA (Option 4) - Config
# =============================================================================
# Delete window - configuration - button 4 root
def open_delete_window() -> None:
    """
    The function opens a window in which the user can enter the site or app they want to delete

    :return: None
    """
    delete_window = Toplevel(root)
    delete_window.iconbitmap(icon)
    delete_window.geometry('350x100')
    delete_window.title('Delete Data')

    delete_label = Label(delete_window, text='Enter a name of site or application that you want to delete:')
    delete_label.pack()
    delete_input = Entry(delete_window, width=40)
    delete_input.pack()

    delete_button = Button(delete_window, text='Delete the data',
                           command=lambda: delete_website_data(delete_input, delete_window))
    delete_button.pack()


# Delete website from database
def delete_website_data(site_input_arg: tkinter.Entry, window: tkinter.Toplevel) -> None:
    """
    The function deletes entered earlier (in open_delete_window) parameter from database

    :param site_input_arg: tkinter.Entry
    :param window: tkinter.Toplevel
    :return: None
    """
    global data
    site = site_input_arg.get().lower()
    if site == '':
        messagebox.showwarning(title='Warning', message='You must enter a site or app you wish to delete!')
    elif site not in data:
        messagebox.showwarning(title="Warning", message=f"Website: {site} is not in database")
    elif site == 'log_in_psw' or site == 'backup':
        messagebox.showwarning(title="Error", message="Permission denied! ")
    else:
        messagebox.showinfo(title='Success', message=f'{site} data successfully deleted')
        del data[site]
        save_data(passwords_file_path, data)
    window.destroy()


# =============================================================================
#                    SHOW SITES OR APPS (Option 5) - Config
# =============================================================================
# Show available sites - button 5 root
def show_sites() -> None:
    """
    The function shows messagebox of all sites whose in data

    :return: None
    """
    global data
    # Make list of sites without 'backup' and 'log_in_psw'
    sites = [x for x in data.keys() if (x != "user_email" and x != "log_in_psw")]
    sites_info = []
    site_number = 1
    for site in sites:
        sites_info.append(f'{site_number}.{site}')
        site_number += 1

    message = "\n".join(sites_info)

    if not sites:
        messagebox.showinfo(title='No pages to view', message='No apps or site in database')
    else:
        messagebox.showinfo(title='Websites and apps in database', message=f'{message}')


# =============================================================================
#                SEARCH LOGIN DATA BY WEBSITE (Option 6) - Config
# =============================================================================
# Search for password - configuration - button 6 root
def open_search_login_details_by_site_window() -> None:
    """
    The function open window in which user enter a name of app/site whose data wants to display

    :return: None
    """
    search_window = Toplevel(root)
    search_window.iconbitmap(icon)
    search_window.geometry('350x100')
    search_window.title('Search for Data')

    search_label = Label(search_window, text='Enter the name of the site or application you want data for')
    search_label.pack()
    search_input = Entry(search_window, width=40)
    search_input.pack()

    search_button = Button(search_window, text='Search for data',
                           command=lambda: search_info(search_input, search_window))
    search_button.pack()


# Searching for data of available sites
def search_info(site_input_arg: tkinter.Entry, window: tkinter.Toplevel) -> None:
    """
    The function show data of entered app/site

    :param site_input_arg: tkinter.Toplevel
    :param window: tkinter.Entry
    :return: None
    """
    global data

    site = site_input_arg.get().lower()
    if site == '':
        messagebox.showwarning(title='Warning', message='You must enter a site/app!')
    elif site not in data:
        messagebox.showwarning(title="Warning", message=f"Website/App: {site} is not in database")
    elif site == 'log_in_psw' or site == 'user_email':
        messagebox.showwarning(title="Error", message="Permission denied! ")
    else:
        site_accounts = data[site]
        login_info = []
        site_number = 1
        for account in site_accounts:
            if 'login' in account and 'password' in account:
                login = account['login']
                password = account['password']
                login_info.append(f"{site_number}. Login: {login} | Password: {password}")
                site_number += 1

        if login_info:
            message = "\n".join(login_info)
            messagebox.showinfo(title=f'Your {site} login details', message=message)

    window.destroy()


# =============================================================================
#                CHANGE SITE OR APP DATA (Option 7) - Config
# =============================================================================
# Change login data - window configuration - button 7 root
def open_check_site_window() -> None:
    """
    The function open check site window in which user input web/app to change data

    :return: None
    """
    check_site_window = Toplevel(root)
    check_site_window.iconbitmap(icon)
    check_site_window.geometry('300x100')
    check_site_window.title('Change Data')

    check_site_label = Label(check_site_window, text='Enter a website or application to change')
    check_site_label.pack()
    check_site_input = Entry(check_site_window, width=35)
    check_site_input.pack()

    check_site_button = Button(check_site_window, text='Check if the website or application is in data',
                               command=lambda: check_if_site_in_data(check_site_input, check_site_window))
    check_site_button.pack()


# Checking if site in data to open window to change data
def check_if_site_in_data(check_site_arg: tkinter.Entry, window: tkinter.Toplevel) -> None:
    """
    The function checks if input site/app is in data and if it exists opens function select_data_from_the_list_window()

    :param check_site_arg: tkinter.Entry
    :param window: tkinter.Toplevel
    :return: None
    """
    global data

    site_to_check = check_site_arg.get().lower()

    if site_to_check == '':
        messagebox.showerror(title='Error', message='Any field cannot be empty!')
    elif site_to_check == 'log_in_psw' or site_to_check == 'user_email':
        messagebox.showwarning(title="Error", message="Website or application is not in data ")

    elif site_to_check in data:
        select_data_from_the_list_window(site_to_check)
    else:
        messagebox.showerror(title='Error', message='Website or application is not in data')

    window.destroy()


# Program ask user which data he wants to change
def select_data_from_the_list_window(site_to_check: str) -> None:
    """
    The function opens window in which all existing data is displayed and then ask user which of data wants to change

    :param site_to_check: str
    :return: None
    """
    select_data_window = Toplevel(root)
    select_data_window.iconbitmap(icon)
    select_data_window.title('Enter number from the list')

    select_data_label = Label(select_data_window,
                              text='Enter number of the data from the list that you want to change:')
    select_data_label.pack()

    site_accounts = data[site_to_check]
    login_info = []
    site_number = 1
    for account in site_accounts:
        if 'login' in account and 'password' in account:
            login = account['login']
            password = account['password']
            login_info.append(f"{site_number}. Login: {login} | Password: {password}\n")
            site_number += 1

    message = "\n".join(login_info)

    available_data_label = Label(select_data_window, text=f'{message}')
    available_data_label.pack()

    select_input = Entry(select_data_window)
    select_input.pack()

    select_button = Button(select_data_window, text='Select',
                           command=lambda: open_input_new_data_window(site_to_check, int(select_input.get()),
                                                                      select_data_window))
    select_button.pack()


# After checking if site is in data, we open input new data window
def open_input_new_data_window(site_to_check: str, selected_index: int, window: tkinter.Toplevel) -> None:
    """
    The function opens window in which user input new login and password

    :param site_to_check: str
    :param selected_index: int
    :param window: tkinter.Toplevel
    :return: None
    """
    try:
        select = selected_index - 1
        if 0 <= select < len(data[site_to_check]):
            change_data_window = Toplevel(root)
            change_data_window.iconbitmap(icon)
            change_data_window.geometry('300x125')
            change_data_window.title('Change Data')

            change_login_label = Label(change_data_window, text='Enter new login')
            change_login_label.pack()
            change_login_input = Entry(change_data_window)
            change_login_input.pack()

            change_password_label = Label(change_data_window, text='Enter new password')
            change_password_label.pack()
            change_password_input = Entry(change_data_window)
            change_password_input.pack()

            change_data_button = Button(change_data_window, text='Change data',
                                        command=lambda: change_data(site_to_check, change_login_input,
                                                                    change_password_input, select, change_data_window))
            change_data_button.pack()

            window.destroy()
        else:
            messagebox.showwarning(title='Error', message='Invalid selection')
    except ValueError:
        messagebox.showwarning(title='Error', message='Invalid input. Please enter a valid number.')


# Changing existing data - function configuration
def change_data(site_to_check: str, login_to_change_arg: tkinter.Entry, password_to_change_arg: tkinter.Entry,
                select: int, window: tkinter.Toplevel) -> None:
    """
    The function takes given parameters, makes them variable and change existing data against the variables

    :param site_to_check: str
    :param login_to_change_arg: tkinter.Entry
    :param password_to_change_arg: tkinter.Entry
    :param select: int
    :param window: tkinter.Toplevel
    :return: None
    """
    global data
    login_to_change = login_to_change_arg.get()
    password_to_change = password_to_change_arg.get()

    if login_to_change == '' or password_to_change == '':
        messagebox.showwarning(title='Error', message='Any field cannot be empty!')
    else:
        data[site_to_check][select]["login"] = login_to_change
        data[site_to_check][select]["password"] = password_to_change
        save_data(passwords_file_path, data)
        messagebox.showinfo(title="Success", message="Data changed successfully")
    window.destroy()


# =============================================================================
#                CLEAR DATABASE (Option 8) - Config
# =============================================================================
# Clear database - popup configuration
def clear_database_popup() -> None:
    """
    The function opens popup which ask if user wants to delete database

    :return: None
    """
    global data
    response = messagebox.askquestion("Clear database", 'Are you sure?')
    if response == 'yes':
        messagebox.showinfo(title="Info", message="You cleared the database.")
        data = {}
        save_data(passwords_file_path, data)
    else:
        messagebox.showinfo(title="Info", message="You did not clear the database.")


# =============================================================================
#         SAVE DATABASE COPY INTO ANOTHER FILE (Option 9) - Config
# =============================================================================
# Save copy into another file - window configuration - button 9
def open_save_copy_window() -> None:
    """
    The function opens save copy window

    :return: None
    """
    save_copy_window = Toplevel(root)
    save_copy_window.iconbitmap(icon)
    save_copy_window.geometry('350x100')
    save_copy_window.title('Save copy into another file')

    save_copy_label = Label(save_copy_window, text='Enter new file name')
    save_copy_label.pack()
    save_copy_input = Entry(save_copy_window, width=50)
    save_copy_input.pack()

    save_copy_button = Button(save_copy_window, text='Save copy',
                              command=lambda: save_copy(save_copy_input, data, save_copy_window))
    save_copy_button.pack()


# Saving copy in the new path
def save_copy(new_file_name_arg: tkinter.Entry, data_arg: Dict, window: tkinter.Toplevel) -> None:
    """
    The function saves copy of data into input path

    :param new_file_name_arg: tkinter.Entry
    :param data_arg: Dict
    :param window: tkinter.Toplevel
    :return: None
    """
    desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
    new_file_name = desktop + "\\" + new_file_name_arg.get()

    if not new_file_name:
        messagebox.showerror(title="Error", message="Path cannot be empty!")
    else:
        save_data(new_file_name, data_arg)

    window.destroy()


# =============================================================================
#                   SAVE DATA AND EXIT (Option 10) - Config
# =============================================================================
# Save data and exit - button 10
def save_and_exit() -> None:
    """
    The function saves data and end ends the program

    :return: None
    """
    save_data(passwords_file_path, data)
    root.quit()
    messagebox.showinfo(title='Success', message='Data saved successfully')


# =============================================================================
#                            ROOT CONFIGURATION
# =============================================================================
# Root configuration
def open_root() -> None:
    """
    The function opens root and all root configuration

    :return: None
    """
    global root
    global b_choice_0, b_choice_1, b_choice_2, b_choice_3, b_choice_4, b_choice_5, b_choice_6, b_choice_7, b_choice_8, b_choice_9, b_choice_10

    root = Tk()
    root.title('Password Manager')
    root.iconbitmap(icon)
    root.geometry('300x710')
    # Define root buttons
    b_choice_0 = Button(root, text='Login', padx=10, pady=10, command=decide_set_or_entry)
    b_choice_1 = Button(root, text='Change password', padx=10, pady=10,
                        command=lambda: open_password_checking_window('Change Password'))
    b_choice_2 = Button(root, text='Change Email', padx=10, pady=10,
                        command=lambda: open_password_checking_window('Change Email'))
    b_choice_3 = Button(root, text='Add new password to the database', padx=10, pady=10, command=open_new_data_window)
    b_choice_4 = Button(root, text='Delete password from the database', padx=10, pady=10, command=open_delete_window)
    b_choice_5 = Button(root, text='Show applications or websites', padx=10, pady=10, command=show_sites)
    b_choice_6 = Button(root, text='Search login details by website', padx=10, pady=10,
                        command=open_search_login_details_by_site_window)
    b_choice_7 = Button(root, text='Change login data', padx=10, pady=10, command=open_check_site_window)
    b_choice_8 = Button(root, text='Clear database', padx=10, pady=10,
                        command=lambda: open_password_checking_window('Clear Database'))
    b_choice_9 = Button(root, text='Save copy in another file', padx=10, pady=10, command=open_save_copy_window)
    b_choice_10 = Button(root, text='Close the program and save the data', padx=10, pady=10, command=save_and_exit)

    # Packing root buttons
    b_choice_0.grid(row=1, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_1.grid(row=2, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_2.grid(row=3, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_3.grid(row=4, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_4.grid(row=5, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_5.grid(row=6, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_6.grid(row=7, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_7.grid(row=8, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_8.grid(row=9, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_9.grid(row=10, column=2, columnspan=1, pady=10, sticky="nsew")
    b_choice_10.grid(row=11, column=2, columnspan=1, pady=10, sticky="nsew")

    # Disable all buttons until user log in
    disable_all_buttons()

    # Adjusting root column and row to center buttons
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_rowconfigure(12, weight=1)


def main() -> None:
    global data

    load_data()
    open_root()
    root.mainloop()


if __name__ == "__main__":
    main()
