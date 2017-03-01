'''
Created on 2017年2月8日

@author: hjg
'''

import datetime

from numpy import array
import numpy
import pandas
from pandas.core.frame import DataFrame
from sklearn.svm.classes import SVR

from com.utils import calSectionId, calDistance


def train(driverSpeed,sectionSpeed,newData,firstTime,n,minLon, lonLen, minLat, latLen,defaultVel):
    '''返回SVR,由[路段平均速度，个人平均速度，载客信息]->瞬时速度训练得到'''
    X=[]
    Y=[]    
    for file in newData:
        df=pandas.read_csv(file, 
                           header=None, 
                           names=["taxiId","lat","lon","busy","time","vel","sec"], 
                           dtype={"taxiId":numpy.int16,"lat":numpy.float32,"lon":numpy.float32,
                                  "busy":numpy.int8,"time":numpy.str,"vel":numpy.float32,
                                  "sec":numpy.int16})
        
        taxiId1=-1
        sectionId1=0
        busy1=0
        time1=firstTime
        for row in df.itertuples(index=False):
            taxiId2=row[0]
            busy2=row[3]
            time2=datetime.datetime.strptime(row[4],"%Y/%m/%d %H:%M:%S")
            v=row[5]
            sectionId2=row[6]
            if taxiId1==taxiId2 and time1.hour==time2.hour and not numpy.isnan(v):
                #前一个点额瞬时速度
                Y.append(v)
                x=[]
                #路段平均速度
                v=sectionSpeed[sectionId1][time1.hour-firstTime.hour]
                if numpy.isnan(v):
                    x.append(defaultVel)
                else:
                    x.append(v)
                #个人平均速度
                v=driverSpeed[taxiId1-1][time1.hour-firstTime.hour]
                if numpy.isnan(v):
                    x.append(defaultVel)
                else:
                    x.append(v)
                #是否载客
                x.append(busy1)
                X.append(x)
            taxiId1=taxiId2
            busy1=busy2;time1=time2
            sectionId1=sectionId2
    
    clf=SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.2, gamma='auto',
            kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
    clf.fit(X, Y)
    
    return clf

def predict(driverSpeed,sectionSpeed,clf,preFile,firstTime,n,minLon, lonLen, minLat, latLen,defaultVel):
    '''返回预测结果的dataframe'''
    df=pandas.read_csv(preFile,
                       header=None,
                       names=["pathId","taxiId","lat","lon","busy","time"],
                       dtype={"pathId":numpy.int16,"taxiId":numpy.int16,"lat":numpy.float32,
                              "lon":numpy.float32,"busy":numpy.int8,"time":numpy.str})
    pathid1=-1
    taxiId1=-1
    lat1=0
    lon1=0
    sectionId1=0
    busy1=0
    time1=firstTime
    
    T=0.0#路径总时间
    one=[]#结果文件第一列：路径id
    two=[]#结果文件第二列:路径时间
    count=0#路径数
    for row in df.itertuples(index=False): 
        pathid2=row[0]
        lat2=row[2]
        lon2=row[3]
        busy2=row[4]
        time2=datetime.datetime.strptime(row[5],"%Y/%m/%d %H:%M:%S")
        if pathid2==pathid1:
            X=[]
            if sectionId1<len(sectionSpeed) and taxiId1<=len(driverSpeed):
                #路段平均速度
                v=sectionSpeed[sectionId1][time1.hour-firstTime.hour]
                if not numpy.isnan(v):
                    X.append(v)
                #个人平均速度
                v=driverSpeed[taxiId1-1][time1.hour-firstTime.hour]
                if not numpy.isnan(v):
                    X.append(v)
            #是否载客
            X.append(busy1)
            #预测结果列表
            Y=[]
            if len(X)==3:
                arrayX = array(X).reshape((1,-1))
                Y=clf.predict(arrayX)
            else :
                Y=[defaultVel]
            t=calDistance(lon1, lat1, lon2, lat2)/Y[0]
            T+=t
        elif taxiId1!=-1:
            one.append(pathid1)
            two.append(T)
            count+=1
            T=0.0
        pathid1=pathid2;taxiId1=row[1];lat1=lat2;lon1=lon2;
        sectionId1=calSectionId(lon1, lat1,n,minLon, lonLen, minLat, latLen)
        busy1=busy2;time1=time2
    if T>0:
        one.append(pathid1)
        two.append(T)
        count+=1
        
    result=DataFrame({'1':one,'2':two},index=list(range(count)))
    return result
    
