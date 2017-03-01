'''
Created on 2017年2月7日

@author: hjg
'''

import datetime

import numpy
import pandas



def sectionSpeed(numOfHours,numOfDays,newData,firstTime,n,minLon, lonLen, minLat, latLen):
    '''计算路段平均速度[地区号][时段]
        n表示将整个地图分成n*n个网格，地区号是其一维下标'''
    #初始化三维数组speed[地区号][时段][天数],值为i地区j时段第k天的速度
    speed=[]
    for i in range(n*n):
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
        sectionId1=0
        time1=firstTime
        #i地区j时段的速度列表
        temp=[]
        for i in range(n*n):
            li=[]
            temp.append(li)
            for j in range(numOfHours):
                li.append([])
        for row in df.itertuples(index=False):
            taxiId2=row[0]
            time2=datetime.datetime.strptime(row[4],"%Y/%m/%d %H:%M:%S")
            v=row[5]
            sectionId2=row[6]
            if taxiId1==taxiId2 and time1.hour==time2.hour:
                if not numpy.isnan(v):
                    temp[sectionId1][time1.hour-firstTime.hour].append(v)
            taxiId1=taxiId2
            time1=time2
            sectionId1=sectionId2
        for i in range(n*n):
            for j in range(numOfHours):
                    speed[i][j][(time1-firstTime).days]=numpy.mean(temp[i][j])
    
    res=[]
    for i in range(n*n):
        li=[]
        res.append(li)
        for j in range(numOfHours):
            temp=[]
            for v in speed[i][j]:
                if not numpy.isnan(v):
                    temp.append(v)
            li.append(numpy.mean(temp))
    return res