
from PyQt5.QtWidgets import QMainWindow,QMessageBox,QApplication
from PyQt5.uic import loadUi
from time import time
import numpy as np
from UserClass import UserModel
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import confusion_matrix
import json

code = "abcdefghijklmnopqrstuvwxyzABCDEFGHİJKLMNOPQRSTUVWXYZ0123456789"
rdict = dict([ (x[1],x[0]) for x in enumerate(code) ])


class AccountWindow(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        loadUi("UserInterface.ui",self)
        self.setWindowTitle("User authentication via Keyboard")
        self.setFixedSize(400, 700) 
    
        self.ErrorMessage = QMessageBox()
        self.RegisterButton.clicked.connect(self.Register)
        self.LoginButton.clicked.connect(self.Login)
        self.ResetButton.clicked.connect(self.Reset)
        self.TrainButton.clicked.connect(self.Train)
        self.TestButton.clicked.connect(self.Predict)
        self.CompareAll.clicked.connect(self.Compare)
        self.ExportButton.clicked.connect(self.SessionExport)
        
        self.TimePressed  = []
        self.TimeReleased = []
        self.TrainSet     = []
        self.Dwell        = []
        self.Flight       = []
        self.ID = -1
        self.String = ""
        self.PasswordText_3.setText(self.String)
        try:
            self.Accounts = np.load("Accounts\Accounts.npy",allow_pickle=True).tolist()
        except:
            self.Accounts = []
    
    
    
    def SessionExport(self):
        if self.ID < 0:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your are not logged in")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()
        else:
            with open("Sessions.json", "w") as outfile: 
                outfile.write(json.dumps(self.Accounts[self.ID].TrainData)) 
    
    
    
    
    
    def Compare(self):
        
        
        X = []
        y = []
        clf = svm.SVC(kernel=self.comboBox.currentText())
        
        for i in range(len(self.Accounts)):
            if self.CompareText.text() == self.Accounts[i].AccountPassword:
                X = X + self.Accounts[i].TrainData
                for x in range(len(self.Accounts[i].TrainData)):
                    y.append(self.Accounts[i].AccountName)
        
        if X == []:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("There are no passwords")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()  
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)       
            clf.fit(X_train,y_train)       
            arr = np.array2string(confusion_matrix(y_test,clf.predict(X_test)))
            self.CompareAllText.setText(arr +" "+str(round(clf.score(X_test,y_test),2)))
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def ProcessData(self):
        
        self.Dwell = np.subtract(self.TimeReleased,self.TimePressed).tolist()
        for i in range(len(self.TimePressed)-1):
                self.Flight.append(self.TimePressed[i+1] - self.TimeReleased[i])
            
        
        
        value = min(self.TimePressed) 
        for i in range(len(self.TimePressed)):
            self.TimePressed[i]  = self.TimePressed[i] - value
        value = min(self.TimeReleased) 
        for i in range(len(self.TimeReleased)):
            self.TimeReleased[i] =self.TimeReleased[i] - value
                
        self.TimePressed  = [ round(x,2) for x in self.TimePressed  ]
        self.TimeReleased = [ round(x,2) for x in self.TimeReleased ]
        self.Dwell        = [ round(x,2) for x in self.Dwell        ]
        self.Flight       = [ round(x,2) for x in self.Flight       ]
    
    
    def Predict(self):
        if self.ID < 0:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your are not logged in")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()
        elif  self.String == self.Accounts[self.ID].AccountPassword:
           
            self.ProcessData()
            
                
                
            model = self.Accounts[self.ID].CreateModel()
            pred = model.predict([self.TimePressed+self.TimeReleased+self.Dwell+self.Flight])
            
            if pred[0] == -1:
                self.TrainText.setText("Your password does not match with the user model")
            else:
                self.TrainText.setText("Your model is matched")

            self.Reset()
        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your password is wrong")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()  
        
        
        
        
        
        
        
    """
      Holds password datas into an array
      If password is correct then the model trained number is increased
      If not logged in doesnt work
    """  
    def Train(self):
        
        if self.ID < 0:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your are not logged in")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()
        elif  self.String == self.Accounts[self.ID].AccountPassword:
            
            
            
            self.ProcessData()
                
            
            self.Accounts[self.ID].AddTrainSet([self.TimePressed+self.TimeReleased+self.Dwell+self.Flight])
            np.save("Accounts\Accounts", self.Accounts,allow_pickle=True)
            
            
            
            
            size = len(self.Accounts[self.ID].TrainData)
            self.TrainText.setText("Your data base increased to {}".format(size))
            self.Reset()
        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your password is wrong")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()  
        
        
        
        
        
        
        
    "The whole data gathered is cleared on this function"
    def Reset(self):
        self.String = ""
        self.TimePressed = []
        self.TimeReleased = []
        self.Dwell        = []
        self.Flight       = []
        self.PasswordText_3.setText(self.String)
    
    """
    It creates accounts by evaluating security rules and saves them into a numpy folder for future use;
    Your ID size must be greater than 6
    Your Password size must be greater than 6
    Your ID must be unique from database IDs
    """
    def Register(self):
        
        if len(self.UserIDText_1.text()) >= 6 and len(self.PasswordText_1.text()) >= 6:
            check = False
            for i in range(len(self.Accounts)):
                if self.UserIDText_1.text() == self.Accounts[i].AccountName:
                    check = True
                
            if check == True:
                self.ErrorMessage.setIcon(QMessageBox.Information)
                self.ErrorMessage.setText("There is a person has that account name")
                self.ErrorMessage.setWindowTitle("Warning!")
                retval = self.ErrorMessage.exec_()       
            else:
                person = UserModel(self.UserIDText_1.text(),self.PasswordText_1.text())
                self.Accounts.append(person)
                np.save("Accounts\Accounts", self.Accounts,allow_pickle=True)
                self.RegistrationText.setText("Registration is completed. Thank you " + person.AccountName) 
        
        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your ID and Password Must be greater than 6 letters")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()    
        
    """
    It controls account data base to confirm you are the person which has the account password correct
    It searches for account ID 
    It controls password
    Then all of them succeed you are assigned as ID number of the account for future uses
        
    """
    def Login(self):
        ID = -1
        for i in range(len(self.Accounts)):
            if self.UserIDText_2.text() == self.Accounts[i].AccountName:
                ID = i
        if ID >= 0:
            if self.Accounts[ID].AccountPassword == self.PasswordText_2.text():
                self.ID = ID
                self.LoginText.setText("You are logged in " + self.Accounts[ID].AccountName + ". Welcome " )
                
            else:
                self.ErrorMessage.setIcon(QMessageBox.Information)
                self.ErrorMessage.setText("Your Password is Wrong")
                self.ErrorMessage.setWindowTitle("Warning!")
                retval = self.ErrorMessage.exec_()
        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("There is no account has this name")
            self.ErrorMessage.setWindowTitle("Warning!")
            retval = self.ErrorMessage.exec_()
    """
    It takes time stamp of password keys
    It controls resetting and unwanted keys
    It generates password label text
    """
    def keyPressEvent(self,event):
        tm = time()
        try:
            convertion = rdict[event.text()]
            self.String += event.text()
            self.TimePressed.append(tm)
        except:
            if 16777219 == event.key():
                self.Reset()
            if 16777220 == event.key():
                self.Train()
        self.PasswordText_3.setText(self.String)
    """
    It takes time stamp of password keys
    It controls resetting and unwanted keys
    It generates password label text
    """
    def keyReleaseEvent(self,event):
        tm = time()
        try:
            convertion = rdict[event.text()]
            self.TimeReleased.append(tm)
        except:
            if 16777219 == event.key():
                self.Reset()
        

    
         
         


app = QApplication([])
window = AccountWindow()
window.show()
app.exec_()