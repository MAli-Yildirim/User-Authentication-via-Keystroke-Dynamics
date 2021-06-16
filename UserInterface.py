from operator import mul
from sklearn.cluster import KMeans,Birch
from PyQt5.QtWidgets import QMainWindow,QMessageBox,QApplication
from PyQt5.uic import loadUi
from time import time
from numpy import load,subtract,save,array2string,array
import numpy as np
from UserClass import UserModel
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC,OneClassSVM

from sklearn.metrics import confusion_matrix,f1_score
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope

from scipy.stats import multivariate_normal
from json import dumps
from sys import argv

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
        self.Reset()
        try:
            self.Accounts = load("Accounts\Accounts.npy",allow_pickle=True).tolist()
        except:
            self.Accounts = []
        
        
          
    
    def SessionExport(self):
        if self.ID < 0:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your are not logged in")
            self.ErrorMessage.setWindowTitle("Warning!")
            self.ErrorMessage.exec_()
        else:
            with open("Sessions.json", "w") as outfile: 
                outfile.write(dumps(self.Accounts[self.ID].TrainData)) 
    
    
    
    
    
    def Compare(self):
        
        
        X = []
        y = []
        self.clf = SVC(kernel=self.comboBox.currentText())
        
        for i in range(len(self.Accounts)):
            if self.CompareText.text() == self.Accounts[i].AccountPassword:
                hold = []
                for k in range(len(self.Accounts[i].TrainData)):
                    hold.append(self.Accounts[i].TrainData[k][16:])
                X = X + hold
                for x in range(len(self.Accounts[i].TrainData)):
                    y.append(self.Accounts[i].AccountName)
        
        


        if X == []:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("There are no passwords")
            self.ErrorMessage.setWindowTitle("Warning!")
            self.ErrorMessage.exec_()  
        elif len(list(set(y))) > 1:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)       
            self.clf.fit(X_train,y_train)       
            arr = array2string(confusion_matrix(y_test,self.clf.predict(X_test)))
            self.CompareAllText.setText(arr +" "+str(round(self.clf.score(X_test,y_test),2)))
        else:
            self.CompareAllText.setText("There are not enough imposter data")
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def ProcessData(self):
        
        self.Dwell = subtract(self.TimeReleased,self.TimePressed).tolist()
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
            self.ErrorMessage.exec_()
        elif  self.String == self.Accounts[self.ID].AccountPassword:
            y = []
            for i in range(len(self.Accounts)):
                if self.Accounts[self.ID].AccountPassword == self.Accounts[i].AccountPassword:
                    for x in range(len(self.Accounts[i].TrainData)):
                        y.append(self.Accounts[i].AccountName)


            sts = len(list(set(y)))

            self.ProcessData()
            

            
                

                

            Xset = []
            Yset = []
            sz = len(self.Accounts[self.ID].AccountPassword)*2

            for j in range(len(self.Accounts[self.ID].TrainData)):
                Xset.append(array(self.Accounts[self.ID].TrainData)[j][sz:])
                Yset.append(1)
            
            Xset = array(Xset)
            Yset = array(Yset)

            

            trainx, testx, trainy, testy = train_test_split(Xset, Yset, test_size=0.3, random_state=2)

            trainx = array(trainx)

            X = []
            multiy = []
            multi2y = []

            if sts > 1:
                
                for i in range(len(self.Accounts)):
                    if self.Accounts[self.ID].AccountPassword == self.Accounts[i].AccountPassword and self.ID != i:
                        hold = []
                        for k in range(len(self.Accounts[i].TrainData)):
                            hold.append(self.Accounts[i].TrainData[k][16:])
                        X = X + hold
                        for x in range(len(self.Accounts[i].TrainData)):
                            multiy.append(-1)
                            multi2y.append(0)
                X = array(X)
                multiy = array(multiy)
                multi2y = array(multi2y)    


                testx = np.concatenate((testx,X))
                testymone = np.concatenate((testy,multiy))
                testymzero = np.concatenate((testy,multi2y))

            if sts == 1:
                testymone  = testy
                testymzero = testy
            
            

            Osvm = OneClassSVM(kernel = 'rbf',gamma="auto").fit(trainx)
            Ypredict = Osvm.predict(testx)
            score = f1_score(testymone, Ypredict, pos_label=1)


            kmeans = KMeans(n_clusters=2, random_state=0).fit(trainx)
            Ypredict = kmeans.predict(testx)
            score1 = f1_score(testymzero, Ypredict, pos_label=1)
                

            brc = Birch(n_clusters=2,threshold=0.01).fit(trainx)
            Ypredict = brc.predict(testx)
            score2 = f1_score(testymzero, Ypredict, pos_label=1)

            IsF = IsolationForest(contamination=0.01)
            IsF.fit(trainx)
            Ypredict = IsF.predict(testx)
            score3 = f1_score(testymone, Ypredict, pos_label=1)
                

            ev = EllipticEnvelope(contamination=0.01)
            ev.fit(trainx)
            Ypredict = ev.predict(testx)
            score4 = f1_score(testymone, Ypredict, pos_label=1)

            if Osvm.predict([self.Dwell+self.Flight]) == 1:
                OsvmResult = 'pass'
            else:
                OsvmResult = 'fail'

            if kmeans.predict([self.Dwell+self.Flight]) == 1:
                kmResult = 'pass'
            else:
                kmResult = 'fail'

            if brc.predict([self.Dwell+self.Flight]) == 1:
                brcResult = 'pass'
            else:
                brcResult = 'fail'

            if IsF.predict([self.Dwell+self.Flight]) == 1:
                IsFResult = 'pass'
            else:
                IsFResult = 'fail'

            if ev.predict([self.Dwell+self.Flight]) == 1:
                evResult = 'pass'
            else:
                evResult = 'fail'

            #print(score,score1,score2,score3,score4)

            self.TrainText.setText("Score/Model"+" \n" + str(round(score,2)) + " Osvm: "+ OsvmResult + " \n"+str(round(score1,2)) +" Km: " + kmResult + " \n"+str(round(score2,2)) +" Brc: "+ brcResult + " \n " +str(round(score3,2)) + " ISF: "+ IsFResult + " \n"+str(round(score4,2)) +" Ev: "+ evResult  )
               


            #if sts > 1:
            #    self.CompareText.setText(self.Accounts[self.ID].AccountPassword)
            #    self.Compare()
            #    prediction = self.clf.predict([self.Dwell+self.Flight])
            #    str1 = str(prediction)
            #    self.TrainText.setText(str(prediction))
            

            self.Reset()


        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your password is wrong")
            self.ErrorMessage.setWindowTitle("Warning!")
            self.ErrorMessage.exec_()  
        
        
        
        
        
        
        
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
            self.ErrorMessage.exec_()
        elif  self.String == self.Accounts[self.ID].AccountPassword:
            
            
            
            self.ProcessData()
                
            
            self.Accounts[self.ID].AddTrainSet([self.TimePressed+self.TimeReleased+self.Dwell+self.Flight])
            save("Accounts\Accounts", self.Accounts,allow_pickle=True)
            
            
            
            
            size = len(self.Accounts[self.ID].TrainData)
            self.TrainText.setText("Your data base increased to {}".format(size))
            self.Reset()
        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your password is wrong")
            self.ErrorMessage.setWindowTitle("Warning!")
            self.ErrorMessage.exec_()  
        
        
        
        
        
        
        
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
                self.ErrorMessage.exec_()       
            else:
                person = UserModel(self.UserIDText_1.text(),self.PasswordText_1.text())
                self.Accounts.append(person)
                save("Accounts\Accounts", self.Accounts,allow_pickle=True)
                self.RegistrationText.setText("Registration is completed. Thank you " + person.AccountName) 
        
        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("Your ID and Password Must be greater than 6 letters")
            self.ErrorMessage.setWindowTitle("Warning!")
            self.ErrorMessage.exec_()    
        
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
                self.ErrorMessage.exec_()
        else:
            self.ErrorMessage.setIcon(QMessageBox.Information)
            self.ErrorMessage.setText("There is no account has this name")
            self.ErrorMessage.setWindowTitle("Warning!")
            self.ErrorMessage.exec_()
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
        

    
         
         


app = QApplication(argv)
window = AccountWindow()
window.show()
app.exec_()