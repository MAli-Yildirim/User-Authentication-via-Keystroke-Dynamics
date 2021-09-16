from numpy.core.fromnumeric import argmax
from sklearn.svm import OneClassSVM , SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,f1_score
from sklearn.cluster import KMeans,Birch
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
import numpy as np


from .models import Data








def CompareAll(code,kernel = 'linear'):

    X = []
    y = []
    X_train, X_test, y_train, y_test = [],[],[],[]
    clf = SVC(kernel=kernel,C=200,probability=True,decision_function_shape='ovo',tol=0.000001,shrinking=False)

    array = Data.objects.filter(code=code)
    le=len(code)*2
    for i in range(len(array)):
        hold = []
        for j in range(len(array[i].content)):
            hold.append((array[i].content)[j][le:])

        X = X + hold
        for x in range(len(array[i].content)):
            y.append(array[i].author.username)

   

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)       
    clf.fit(X_train,y_train)       
    arr = confusion_matrix(y_test,clf.predict(X_test))
    return arr , str(round(clf.score(X_test,y_test),2)) , clf


def Predict(username,code,classcode):
    X = []
    y = []
   
    userx = []
    usery = []
    impx  = []
    impy  = []
    impymin = []
    array = Data.objects.filter(code=code)
    le=len(code)*2
    for i in range(len(array)):
        hold = []
        for j in range(len(array[i].content)):
            hold.append((array[i].content)[j][le:])

        X = X + hold
        for x in range(len(array[i].content)):
            y.append(array[i].author.username)

    for k in range(len(y)):
        if y[k] == username:
            userx.append(X[k])
            usery.append(1)
        else:
            impx.append(X[k])
            impy.append(0) 
            impymin.append(-1) 


  
    for a in range(len(y)):
        if y[a] == username:
            y[a] = 1
        else:
            y[a] = 0



    userx   = np.array(userx)
    usery   = np.array(usery)
    impx    = np.array(impx)
    impy    = np.array(impy)
    impymin = np.array(impymin)

 

    



    userX_train, userX_test, usery_train, usery_test = train_test_split(userx, usery, test_size=0.1, random_state=2)
    

   
  
    

    testx = np.concatenate((userX_test,impx))
    testy = np.concatenate((usery_test,impy))

    trainx = np.concatenate((userX_train,impx))
    
    

    testymin = np.concatenate((usery_test,impymin))
 
  
    Osvm = OneClassSVM(kernel = 'rbf',gamma="auto").fit(userX_train)
    Ypredict = Osvm.predict(testx)
    score = f1_score(testymin, Ypredict, pos_label=1)

    kmeans = KMeans(n_clusters=2, random_state=0).fit(trainx)
    Ypredict = kmeans.predict(userX_test)
    score1 = f1_score(usery_test, Ypredict, pos_label=1)

    brc = Birch(n_clusters=2,threshold=0.01).fit(trainx)
    Ypredict = brc.predict(userX_test)
    score2 = f1_score(usery_test, Ypredict, pos_label=1)

    IsF = IsolationForest(contamination=0.01)
    IsF.fit(userX_train)
    Ypredict = IsF.predict(testx)
    score3 = f1_score(testymin, Ypredict, pos_label=1)

    ev = EllipticEnvelope(contamination=0.01)
    ev.fit(userX_train)
    Ypredict = ev.predict(testx)
    score4 = f1_score(testymin, Ypredict, pos_label=1)

    scores = [round(score,2),round(score1,2),round(score2,2),round(score3,2),round(score4,2)]
    scores = np.array(scores)
    index =  np.argmax(scores)
    scorestring = scores[index]
    string3 = 'F2 score is: ' + str(scorestring)

    if   index == 0:
        model = Osvm
        string1 = 'Osvm is selected'
        
    elif index == 1:
        model = kmeans
        string1 = 'kmeans is selected'
    elif index == 2:
        model = brc
        string1 = 'brc is selected'
    elif index == 3:
        model = IsF
        string1 = 'Isf is selected'
    elif index == 4:
        model = ev
        string1 = 'ev is selected'

    
    if model.predict(classcode) == 1:
        string2 = 'Your model matched'
    else:
        string2 = 'Your model is not matched'











    return string1,string2,string3,scores,index+1
