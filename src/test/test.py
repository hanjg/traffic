'''
Created on 2017年2月7日

@author: hjg
'''
import datetime

import numpy
import pandas
from sklearn import svm
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from numpy import array


def svm():
    X = [[0, 0], [2, 2]]  
    y = [0.5, 2.5]  
    clf = svm.SVR(C=1, cache_size=200, coef0=0.0, degree=3, epsilon=0.2, gamma='auto',
    kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
    clf.fit(X, y) 
    print(clf.predict([[1, 1]])) 

def dftime():
    df=pandas.read_csv("exampleLongitude.txt", header=None, names=["taxiId","lat","lon","busy","time"], 
                           dtype={"taxiId":numpy.int16,"lat":numpy.double,"lon":numpy.double,
                                  "busy":numpy.int8,"time":numpy.str})

    print(df.iloc[0][4])
    print(datetime.datetime.strptime("2014/8/3 21:18:46","%Y/%m/%d %H:%M:%S"))
    time1=datetime.datetime.strptime(df.iloc[0][4],"%Y/%m/%d %H:%M:%S")
    time2=datetime.datetime.strptime(df.iloc[1004][4],"%Y/%m/%d %H:%M:%S")
    print(time1-time2)
    print((time1-time2).days)
    print(time1.hour)
    print(datetime.datetime.strptime("2014/8/3","%Y/%m/%d").hour)
def dfsort():
    df=pandas.read_csv("exampleLongitude.txt", header=None, names=["taxiId","lat","lon","busy","time"], 
                           dtype={"taxiId":numpy.int16,"lat":numpy.double,"lon":numpy.double,
                                  "busy":numpy.int8,"time":numpy.str})
    df.sort_values(by=["taxiId","time"], axis=0, ascending=[True,True], inplace=True)
    print(df)

def dfIter():
    df=pandas.read_csv("exampleLongitude.txt", header=None, names=["taxiId","lat","lon","busy","time"], 
                           dtype={"taxiId":numpy.int16,"lat":numpy.double,"lon":numpy.double,
                                  "busy":numpy.int8,"time":numpy.str})
    for row in df.itertuples(index=False):
        print(row[4])
def initList():
    temp=[]
    count=0
    for i in range(3):
        li=[]
        temp.append(li)
        for j in range(5):
            lj=[]
            li.append(lj)
            for k in range(5):
                lj.append(count)
                count+=1
    print(temp)
    print(temp[1][1][1])

def numpyMean():
    a=[1,2,3,4,5,6]
    print(numpy.mean(a))
    
X=[[1,2],[3,4]]
arrayX = array(X).reshape((-1,1))
print(X)

