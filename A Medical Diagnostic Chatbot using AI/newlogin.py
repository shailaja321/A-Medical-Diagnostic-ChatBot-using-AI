# import modules

from tkinter import *
import os


# Designing window for registration
def destroyPackWidget(parent):
    for e in parent.pack_slaves():
        e.destroy()
def register():
    global root,register_screen
    
    destroyPackWidget(root)
    register_screen=root
#    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("400x300")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter the details below", bg="blue", font=("Calibri", 14), fg="white").pack(pady=10)
    username_lable = Label(register_screen, text="Username * ", font=("Calibri", 12))
    username_lable.pack(pady=5)
    username_entry = Entry(register_screen, textvariable=username, font=("Calibri", 12), width=30)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ", font=("Calibri", 12))
    password_lable.pack(pady=5)
    password_entry = Entry(register_screen, textvariable=password, show='*', font=("Calibri", 12), width=30)
    password_entry.pack()
    Button(register_screen, text="Register", width=15, height=2, bg="blue", fg="white", command=register_user).pack(pady=20)


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("400x300")
    Label(login_screen, text="Please enter details below to login").pack(pady=10)

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ", font=("Calibri", 12)).pack(pady=5)
    username_login_entry = Entry(login_screen, textvariable=username_verify, font=("Calibri", 12), width=30)
    username_login_entry.pack()
    Label(login_screen, text="Password * ", font=("Calibri", 12)).pack(pady=5)
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*', font=("Calibri", 12), width=30)
    password_login_entry.pack()
    Button(login_screen, text="Login", width=15, height=2, bg="blue", fg="white", command=login_verify).pack(pady=20)


# Implementing event on register button
def btnSucess_Click():
    global root
    destroyPackWidget(root)
def register_user():
    global root,username,password
    username_info = username.get()
    password_info = password.get()
    print("abc",username_info,password_info,"xyz")
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(root, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    Button(root,text="Click Here to proceed",command=btnSucess_Click).pack()


# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = map(str.lower, os.listdir())  # Case-insensitive matching
    if username1.lower() in list_of_files:
        with open(username1, "r") as file:
            verify = file.read().splitlines()
        if password1 in verify:
            login_sucess()
        else:
            password_not_recognised()
    else:
        user_not_found()



# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()


# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("50x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("50x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Function for forgot password
def forgot_password():
    global forgot_password_screen, forgot_username_entry
    forgot_password_screen = Toplevel(login_screen)
    forgot_password_screen.title("Forgot Password")
    forgot_password_screen.geometry("100x50")
    Label(forgot_password_screen, text="Enter your username to reset password").pack()
    forgot_username = StringVar()

    Label(forgot_password_screen, text="Username * ").pack()
    forgot_username_entry = Entry(forgot_password_screen, textvariable=forgot_username)
    forgot_username_entry.pack()
    Label(forgot_password_screen, text="").pack()
    Button(forgot_password_screen, text="Reset Password", command=lambda: reset_password(forgot_username.get())).pack()

# Function to reset password
def reset_password(username):
    if username.lower() in map(str.lower, os.listdir()):  # Case-insensitive check
        file = open(username, "r")
        verify = file.read().splitlines()
        file.close()

        # Resetting password
        new_password = StringVar()
        Label(forgot_password_screen, text="Enter new password").pack()
        new_password_entry = Entry(forgot_password_screen, textvariable=new_password, show='*')
        new_password_entry.pack()
        Button(forgot_password_screen, text="Submit", command=lambda: save_new_password(username, new_password.get())).pack()
    else:
        Label(forgot_password_screen, text="User not found!", fg="red").pack()

# Function to save new password
def save_new_password(username, new_password):
    with open(username, "w") as file:
        file.write(username + "\n" + new_password)  # Append new password
    Label(forgot_password_screen, text="Password Reset Successful", fg="green").pack()


# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen(frmmain):
    main_screen=frmmain
    
    main_screen.geometry("500x400")
    main_screen.title("Account Login")
    Label(main_screen,text="Select Your Choice", bg="blue", width="100", height="3", font=("Calibri", 13)).pack(pady=20)
    Button(main_screen,text="Login", height="3", width="100", command=login).pack(pady=10)
    Button(main_screen,text="Register", height="3", width="100", command=register).pack(pady=10)

    

root = Tk()
main_account_screen(root)

root.mainloop()
