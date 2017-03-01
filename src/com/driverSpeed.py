'''
Created on 2017年2月7日

@author: hjg
'''
import datetime

import numpy
import pandas


def driverSpeed(numOfDrivers,numOfHours,numOfDays,newData,firstTime):
    '''计算个人平均速度[出租车id][时段]'''
    
    #初始化三维维数组speed[出租车id][时段][天数]，值为i出租车j时段第k天的平均速度
    speed=[]
    for i in range(numOfDrivers):
        li=[]
        speed.append(li)
        for j in range(numOfHours):
            lj=[]
            li.append(lj)
            for k in range(numOfDays):
                lj.append(numpy.nan)
    
    for file in newData:
        df=pandas.read_csv(file, 
                           header=None, 
                           names=["taxiId","lat","lon","busy","time","vel","sec"], 
                           dtype={"taxiId":numpy.int16,"lat":numpy.float32,"lon":numpy.float32,
                                  "busy":numpy.int8,"time":numpy.str,"vel":numpy.float32,
                                  "sec":numpy.int16})
        
        taxiId1=-1
        time1=firstTime
        #i出租车在j时段的速度列表
        temp=[]
        for row in df.itertuples(index=False):
            taxiId2=row[0]
            time2=datetime.datetime.strptime(row[4],"%Y/%m/%d %H:%M:%S")
            v=row[5]
            if taxiId1==taxiId2 and time1.hour==time2.hour:
                if not numpy.isnan(v):
                    temp.append(v)
            elif taxiId1!=-1:
                    speed[taxiId1-1][time1.hour-firstTime.hour][(time1-firstTime).days]=numpy.mean(temp)
                    temp=[]
            taxiId1=taxiId2;time1=time2
        if len(temp)!=0:
            speed[taxiId1-1][time1.hour-firstTime.hour][(time1-firstTime).days]=numpy.mean(temp) 
    #按照天数求平均速度  
    res=[]
    for i in range(numOfDrivers):
        li=[]
        res.append(li)
        for j in range(numOfHours):
            temp=[]
            for v in speed[i][j]:
                if not numpy.isnan(v):
                    temp.append(v)
            li.append(numpy.mean(temp))
    return res