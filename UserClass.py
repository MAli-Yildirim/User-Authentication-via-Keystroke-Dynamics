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
        hold = []
        sz = len(self.AccountPassword)*2

        for j in range(len(self.TrainData)):
            hold.append(array(self.TrainData)[j][sz:])
        return OneClassSVM(kernel = 'rbf',gamma="auto").fit(array(hold))
        
        
    
        
    
    
    