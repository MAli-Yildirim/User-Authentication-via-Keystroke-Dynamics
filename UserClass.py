from sklearn.svm import OneClassSVM
from numpy import array

class UserModel():
    
    def __init__(self,Name,Password):
        self.AccountName = Name
        self.AccountPassword = Password
        self.TrainData    = []
        
    def AddTrainSet(self,TrainSet):
        self.TrainData = self.TrainData + TrainSet
        
    def CreateModel(self):
        return OneClassSVM(kernel = 'rbf', gamma = 0.000001, nu = 0.03).fit(array(self.TrainData))
        
        
    
        
    
    
    