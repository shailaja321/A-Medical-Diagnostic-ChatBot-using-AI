# Importing the libraries
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage                         
import os            
import webbrowser
from numpy.lib.npyio import recursive
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, _tree
# wikipidea, openai

import numpy as np
import pandas as pd

class HyperlinkManager:
      
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# Importing the dataset
training_dataset = pd.read_csv('Training.csv')
test_dataset = pd.read_csv('Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols     = training_dataset.columns
cols     = cols[:-1]

# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

# Implementing the Visual Tree
from sklearn.tree import _tree

# Method to simulate the working of a Chatbot by extracting and formulating questions
def print_disease(node):
        #print(node)
        node = node[0]
        #print(len(node))
        val  = node.nonzero() 
        #print(val)
        disease = labelencoder.inverse_transform(val[0])
        return disease
def recurse(node, depth):
            global val,ans
            global tree_,feature_name,symptoms_present
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                yield name + " ?"
                
#                ans = input()
                ans = ans.lower()
                if ans == 'yes':
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    yield from recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    yield from recurse(tree_.children_right[node], depth + 1)
            else:
                strData=""
                present_disease = print_disease(tree_.value[node])
#                print( "You may have " +  present_disease )
#                print()
                strData="You may have :" +  str(present_disease)
               
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                
                red_cols = dimensionality_reduction.columns 
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
#                print("symptoms present  " + str(list(symptoms_present)))
#                print()
                strData="symptoms present:  " + str(list(symptoms_present))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
#                print("symptoms given "  +  str(list(symptoms_given)) )  
#                print()
                strData="symptoms given: "  +  str(list(symptoms_given))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
#                print("confidence level is " + str(confidence_level))
#                print()
                strData="confidence level is: " + str(confidence_level)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
#                print('The model suggests:')
#                print()
                strData='The model suggests:'
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                row = doctors[doctors['disease'] == present_disease[0]]
#                print('Consult ', str(row['name'].values))
#                print()
                strData='Consult '+ str(row['name'].values)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
#                print('Visit ', str(row['link'].values))
                #print(present_disease[0])
                hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
                strData='Visit '+ str(row['link'].values[0])
                def click1():
                    webbrowser.open_new(str(row['link'].values[0]))
                QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
                #QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                yield strData
        
def tree_to_code(tree, feature_names):
        global tree_,feature_name,symptoms_present
        tree_ = tree.tree_
        #print(tree_)
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        #print("def tree({}):".format(", ".join(feature_names)))
        symptoms_present = []   
#        recurse(0, 1)
    

def execute_bot():
#    print("Please reply with yes/Yes or no/No for the following symptoms")    
    tree_to_code(classifier,cols)



# This section of code to be run after scraping the data

doc_dataset = pd.read_csv('doctors_dataset.csv', names = ['Name', 'Description'])


diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

doctors['disease'] = diseases['prognosis']


doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']

record = doctors[doctors['disease'] == 'AIDS']
record['name']
record['link']




# Execute the bot and see it in Action
#execute_bot()


class QuestionDigonosis(Frame):
    objIter=None
    objRef=None
    def __init__(self,master=None):
        master.title("Question")
        # root.iconbitmap("")
        master.state("z")
#        master.minsize(700,350)
        QuestionDigonosis.objRef=self
        super().__init__(master=master)
        self["bg"]="light blue"
        self.createWidget()
        self.iterObj=None

    def createWidget(self):
        self.lblQuestion=Label(self,text="Question",width=12,bg="bisque")
        self.lblQuestion.grid(row=0,column=0,rowspan=4)

        self.lblDigonosis = Label(self, text="Digonosis",width=12,bg="bisque")
        self.lblDigonosis.grid(row=4, column=0,sticky="n",pady=5)

        # self.varQuestion=StringVar()
        self.txtQuestion = Text(self, width=100,height=4)
        self.txtQuestion.grid(row=0, column=1,rowspan=4,columnspan=20)

        self.varDiagonosis=StringVar()
        self.txtDigonosis =Text(self, width=100,height=14)
        self.txtDigonosis.grid(row=4, column=1,columnspan=20,rowspan=20,pady=5)

        self.btnNo=Button(self,text="No",width=12,bg="bisque", command=self.btnNo_Click)
        self.btnNo.grid(row=25,column=0)
        self.btnYes = Button(self, text="Yes",width=12,bg="bisque", command=self.btnYes_Click)
        self.btnYes.grid(row=25, column=1,columnspan=20,sticky="e")

        self.btnClear = Button(self, text="Clear",width=12,bg="bisque", command=self.btnClear_Click)
        self.btnClear.grid(row=27, column=0)
        self.btnStart = Button(self, text="Start",width=12,bg="bisque", command=self.btnStart_Click)
        self.btnStart.grid(row=27, column=1,columnspan=20,sticky="e")
    def btnNo_Click(self):
        global val,ans
        global val,ans
        ans='no'
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0,END)
        self.txtQuestion.insert(END,str1+"\n")
        
    def btnYes_Click(self):
        global val,ans
        ans='yes'
        self.txtDigonosis.delete(0.0,END)
        str1=QuestionDigonosis.objIter.__next__()
        
#        self.txtDigonosis.insert(END,str1+"\n")
        
    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
        self.txtDigonosis.insert(END,"Please Click on Yes or No for the Above symptoms in Question")                  
        QuestionDigonosis.objIter=recurse(0, 1)
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END,str1+"\n")

class MainForm(Frame):
    main_Root = None
    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        MainForm.main_Root = master
        super().__init__(master=master)
        master.geometry("800x600")
        master.title("Account Login")
        self.createWidget()
    def createWidget(self):
        # Load the background image
        self.bg_image = PhotoImage(file=r"C:/Users/shail/OneDrive/Documents/Desktop/shailu/mini_proj/A Medical Diagnostic Chatbot using AI/Bgim_Minim.png")  # Replace with your image file path
        self.canvas = Canvas(self, width=1470, height=980)  # Adjust dimensions to match the image
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.lblMsg = Label(self, text="Medical Diagnostic ChatBot", bg="PeachPuff2", width="50", height="2", font=("Calibri", 13))
        self.lblMsg_window = self.canvas.create_window(800, 50, window=self.lblMsg)  # Center the label

        self.btnLogin = Button(self, text="Login", height="2", width="25",command=self.lblLogin_Click , bg="lightgreen", fg="black", font=("Calibri", 17, "bold"))
        self.btnLogin_window = self.canvas.create_window(750, 550, window=self.btnLogin)

        self.btnRegister = Button(self, text="Register", height="2", width="25", command=self.btnRegister_Click, bg="lightgreen", fg="black", font=("Calibri", 17, "bold"))
        self.btnRegister_window = self.canvas.create_window(750, 650, window=self.btnRegister)

        self.lblTeam = Label(self, text="Made by:", bg="slateblue4", width="30", height="1", font=("Calibri", 13))
        self.lblTeam_window = self.canvas.create_window(1300, 600, window=self.lblTeam)

        self.lblTeam1 = Label(self, text="Shailaja", bg="RoyalBlue1", width="30", height="1", font=("Calibri", 13))
        self.lblTeam1_window = self.canvas.create_window(1300, 630, window=self.lblTeam1)

        self.lblTeam2 = Label(self, text="Gowthami", bg="RoyalBlue2", width="30", height="1", font=("Calibri", 13))
        self.lblTeam2_window = self.canvas.create_window(1300, 660, window=self.lblTeam2)

        self.lblTeam3 = Label(self, text="Narender", bg="RoyalBlue3", width="30", height="1", font=("Calibri", 13))
        self.lblTeam3_window = self.canvas.create_window(1300, 690, window=self.lblTeam3)

        self.lblTeam4 = Label(self, text="Akhil", bg="RoyalBlue4", width="30", height="1", font=("Calibri", 13))
        self.lblTeam4_window = self.canvas.create_window(1300, 720, window=self.lblTeam4)

    def lblLogin_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmLogin=Login(MainForm.main_Root)
        frmLogin.pack()
    def btnRegister_Click(self):
        self.destroyPackWidget(MainForm.main_Root)
        frmSignUp = SignUp(MainForm.main_Root)
        frmSignUp.pack()
   

        
class Login(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        Login.main_Root=master
        super().__init__(master=master)
        master.title("Login")
        master.geometry("800x600")
        master.state("zoomed")
        self.createWidget()
    def createWidget(self):
        #Load the bgim image
        self.bg_image = PhotoImage(file=r"C:/Users/shail/OneDrive/Documents/Desktop/shailu/mini_proj/A Medical Diagnostic Chatbot using AI/Bgim_Minim.png")  # Replace with your image file path
        self.canvas = Canvas(self, width= 1470, height= 980)  # Set Canvas to screen size
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")  # Place the image at the top-left corner
        
        # Add widgets on top of the canvas
        self.lblMsg = Label(self, text="ACCOUNT LOGIN", bg="lightblue", font=("Calibri", 12 , "bold"))
        self.lblMsg_window = self.canvas.create_window(200, 100, window=self.lblMsg)

        self.username = Label(self, text="USERNAME * ", bg="lightblue", font=("Calibri", 12 , "bold"))
        self.username_window = self.canvas.create_window(100, 150, window=self.username)

        self.username_verify = StringVar()
        self.username_login_entry = Entry(self, textvariable=self.username_verify)
        self.username_login_entry_window = self.canvas.create_window(250, 150, window=self.username_login_entry)

        self.password = Label(self, text="PASSWORD * ", bg="lightblue", font=("Calibri", 12 , "bold"))
        self.password_window = self.canvas.create_window(100, 200, window=self.password)

        self.password_verify = StringVar()
        self.password_login_entry = Entry(self, textvariable=self.password_verify, show='*')
        self.password_login_entry_window = self.canvas.create_window(250, 200, window=self.password_login_entry)

        self.btnLogin = Button(self, text="LOGIN", width=13, height=1, command=self.btnLogin_Click, bg="green", fg="white", font=("Calibri", 12, "bold"))
        self.btnLogin_window = self.canvas.create_window(100, 250, window=self.btnLogin)

        self.btnForgotPassword = Button(self, text="FORGOT PASSWORD?", width=18, height=1, command=self.btnForgotPassword_Click, bg="orange", fg="white", font=("Calibri", 12, "bold"))
        self.btnForgotPassword_window = self.canvas.create_window(250, 250, window=self.btnForgotPassword)

        self.btnRetrievePasswords = Button(self, text="RETRIEVE PASSWORDS", width=20, height=1, command=self.retrieve_passwords, bg="blue", fg="white", font=("Calibri", 12, "bold"))
        self.btnRetrievePasswords_window = self.canvas.create_window(175, 300, window=self.btnRetrievePasswords)

    def btnLogin_Click(self):
        username1 = self.username_login_entry.get().strip()
        password1 = self.password_login_entry.get().strip()

        if username1 and password1:
            # Check if the username file exists
            if os.path.exists(f"{username1}.txt"):
                try:
                    with open(f"{username1}.txt", "r") as file:
                        lines = file.readlines()
                        saved_username = lines[1].split(":")[1].strip()  # Extract saved username
                        saved_password = lines[2].split(":")[1].strip()  # Extract saved password

                    # Validate the username and password
                    if username1 == saved_username and password1 == saved_password:
                        messagebox.showinfo("Success", "Login Successful!")
                        self.destroyPackWidget(Login.main_Root)
                        frmQuestion = QuestionDigonosis(Login.main_Root)
                        frmQuestion.pack()
                    else:
                        messagebox.showerror("Error", "Invalid username or password. Please try again.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while reading user details: {e}")
            else:
                messagebox.showerror("Error", "User not found. Please register first.")
        else:
            messagebox.showerror("Error", "Both username and password are required.")

    def save_password(self, username, password):
        """Save the username and password to a file."""
        with open("saved_passwords.txt", "a") as file:
            file.write(f"{username}:{password}\n")
        messagebox.showinfo("Success", "Your password has been saved securely.")
    def retrieve_passwords(self):
        """Retrieve and display saved passwords."""
        try:
            with open("saved_passwords.txt", "r") as file:
                saved_passwords = file.readlines()

            if saved_passwords:
                passwords = "\n".join(saved_passwords)
                messagebox.showinfo("Saved Passwords", f"Here are the saved passwords:\n\n{passwords}")
            else:
                messagebox.showinfo("No Passwords Found", "No saved passwords found.")
        except FileNotFoundError:
            messagebox.showinfo("Error", "No saved passwords file found.")
    def btnForgotPassword_Click(self):
        self.destroyPackWidget(Login.main_Root)
        frmForgotPassword = ForgotPassword(Login.main_Root)
        frmForgotPassword.pack()

class ForgotPassword(Frame):
    main_Root = None

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

    def __init__(self, master=None):
        ForgotPassword.main_Root = master
        super().__init__(master=master)
        self.master.title("Forgot Password")
        self.master.geometry("800x600")
        self.master.attributes("-fullscreen", True)
        self.master.bind("<Escape>",self.exit_fullscreen)
        self.createWidget()
    def exit_fullscreen(self,event=None):
        self.master.attributes("-fullscreen",False)
    def createWidget(self):
        #Load the Background image
        self.bg_image = PhotoImage(file=r"C:/Users/shail/OneDrive/Documents/Desktop/shailu/mini_proj/A Medical Diagnostic Chatbot using AI/login_bgim.png")  # Replace with your image file path
        self.canvas = Canvas(self, width=root.winfo_screenwidth(), height=root.winfo_screenheight())  # Adjust dimensions to match the image
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        center_x = self.master.winfo_screenwidth() // 2
        center_y = self.master.winfo_screenheight() // 2

        # Add widgets on the top of the canvas
        self.lblMsg = Label(self, text="FORGOT PASSWORD", bg="lightblue", font=("Calibri", 13, "bold"))
        self.lblMsg_window = self.canvas.create_window(center_x, center_y - 100, window=self.lblMsg)

        self.username_label = Label(self, text="USERNAME * ", bg="lightblue", font=("Calibri", 13, "bold"))
        self.username_label_window = self.canvas.create_window(center_x - 100, center_y - 50, window=self.username_label)

        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username)
        self.username_entry_window = self.canvas.create_window(center_x + 50, center_y - 50, window=self.username_entry)

        self.new_password_label = Label(self, text="NEW PASSWORD * ", bg="lightblue", font=("Calibri", 13 , "bold"))
        self.new_password_label_window = self.canvas.create_window(center_x - 100, center_y, window=self.new_password_label)

        self.new_password = StringVar()
        self.new_password_entry = Entry(self, textvariable=self.new_password, show='*')
        self.new_password_entry_window = self.canvas.create_window(center_x + 50, center_y, window=self.new_password_entry)

        self.btnResetPassword = Button(self, text="RESET PASSWORD", width=15, height=1, command=self.reset_password, bg="green", fg="white", font=("Calibri", 15, "bold"))
        self.btnResetPassword_window = self.canvas.create_window(center_x, center_y + 50, window=self.btnResetPassword)
    
    def reset_password(self):
        username = self.username_entry.get()
        new_password = self.new_password_entry.get()

        if username in os.listdir():
            with open(username, "w") as file:
                file.write(username + "\n")
                file.write(new_password)
            messagebox.showinfo("Success", "Password reset successful. Please log in.")
            self.destroyPackWidget(ForgotPassword.main_Root)
            frmLogin = Login(ForgotPassword.main_Root)
            frmLogin.pack()
        else:
            messagebox.showinfo("Failure", "Username not found. Please try again.")
class SignUp(Frame):
    main_Root = None
    print("SignUp Class")

    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()

    def __init__(self, master=None):
        SignUp.main_Root = master
        master.title("Register")
        super().__init__(master=master)
        master.geometry("800x600")
        master.state("zoomed")
        self.createWidget()

    def createWidget(self):
        # Load the background image
        self.bg_image = PhotoImage(file=r"C:/Users/shail/OneDrive/Documents/Desktop/shailu/mini_proj/A Medical Diagnostic Chatbot using AI/login_bgim.png")  # Replace with your image file path
        self.canvas = Canvas(self, width=1470, height=980)  # Adjust dimensions to match the image
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Add widgets on top of the canvas
        self.lblMsg = Label(self, text="Register to the ChatBot", bg="lightblue", font=("Calibri", 18, "bold"))
        self.lblMsg_window = self.canvas.create_window(400, 100, window=self.lblMsg)

        self.Name_label = Label(self, text="FULL NAME * ", bg="lightblue", font=("Calibri", 16, "bold"))
        self.Name_label_window = self.canvas.create_window(300, 150, window=self.Name_label)

        self.Name = StringVar()
        self.Name_entry = Entry(self, textvariable=self.Name , font=("Times New Roman",16))
        self.Name_entry_window = self.canvas.create_window(500, 150, window=self.Name_entry)

        self.username_label = Label(self, text="USERNAME * ", bg="lightblue", font=("Calibri", 16, "bold"))
        self.username_label_window = self.canvas.create_window(300, 200, window=self.username_label)

        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username, font=("Times New Roman",16))
        self.username_entry_window = self.canvas.create_window(500, 200, window=self.username_entry)

        self.password_label = Label(self, text="PASSWORD * ", bg="lightblue", font=("Calibri", 16, "bold"))
        self.password_label_window = self.canvas.create_window(300, 250, window=self.password_label)

        self.password = StringVar()
        self.password_entry = Entry(self, textvariable=self.password, font=("Times New Roman",16), show='*')
        self.password_entry_window = self.canvas.create_window(500, 250, window=self.password_entry)

        self.btnRegister = Button(self, text="REGISTER", width=15, height=1, bg="green", fg="white", font=("Calibri", 18, "bold"), command=self.register_user)
        self.btnRegister_window = self.canvas.create_window(400, 300, window=self.btnRegister)

    def register_user(self):
        # Automatically save user details to a file
        username = self.username_entry.get().strip()
        full_name = self.Name_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and full_name and password:
            # Check if the username already exists
            if os.path.exists(f"{username}.txt"):
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            else:
                # Save user details to a file
                try:
                    with open(f"{username}.txt", "w") as file:
                        file.write(f"Full Name: {full_name}\n")
                        file.write(f"Username: {username}\n")
                        file.write(f"Password: {password}\n")

                    messagebox.showinfo("Success", "Registration Successful! Your details have been saved.")
                    self.destroyPackWidget(SignUp.main_Root)
                    frmLogin = Login(SignUp.main_Root)
                    frmLogin.pack()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving your details: {e}")
        else:
            messagebox.showerror("Error", "All fields are required. Please fill in all details.")
    def btnSuccess_Click(self):
        self.destroyPackWidget(SignUp.main_Root)
        frmQuestion = QuestionDigonosis(SignUp.main_Root)
        frmQuestion.pack()

root = Tk()

frmMainForm=MainForm(root)
frmMainForm.pack()
root.mainloop()
# Load datasets
testing_dataset = pd.read_csv('Testing.csv')
doc_dataset = pd.read_csv('doctors_dataset.csv', names=['Name', 'Description'])

# Extract symptoms dynamically from the Testing dataset
symptoms_list = testing_dataset.columns[:-1].str.lower().tolist()

# Prepare the doctors dataset
doctors = pd.DataFrame()
doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']
doctors['disease'] = dimensionality_reduction.index

