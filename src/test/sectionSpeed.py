'''
Created on 2017年2月7日

@author: hjg
'''

import datetime

from numpy import math
import numpy
import pandas

from com.utils import calDistance
from com.utils import calSectionId


def sectionSpeed(numOfHours,numOfDays,trainData,firstTime,n,minLon, lonLen, minLat, latLen):
    '''计算路段平均速度[地区号][时段]
        n表示将整个地图分成n*n个网格，地区号是其一维下标'''
    #缺乏数据默认的速度
    defaultVel=5.0
    
    #初始化三维数组speed[地区号][时段][天数],值为i地区j时段第k天的速度
    speed=[]
    for i in range(n*n):
        li=[]
        speed.append(li)
        for j in range(numOfHours):
            lj=[]
            li.append(lj)
            for k in range(numOfDays):
                lj.append(0.0)
    
    for file in trainData:
        df=pandas.read_csv(file, 
                           header=None, 
                           names=["taxiId","lat","lon","busy","time"], 
                           dtype={"taxiId":numpy.int16,"lat":numpy.double,"lon":numpy.double,
                                  "busy":numpy.int8,"time":numpy.str})
        #df按照出租车id，时间点升序排序
        df.sort_values(by=["taxiId","time"], axis=0, ascending=[True,True], inplace=True)
        
        taxiId1=-1
        lat1=0
        lon1=0
        sectionId1=0
        time1=firstTime
        temp=[]
        for i in range(n*n):
            li=[]
        for row in df.itertuples(index=False):
            taxiId2=row[0]
            lat2=row[1]
            lon2=row[2]
            time2=datetime.datetime.strptime(row[4],"%Y/%m/%d %H:%M:%S")
            if taxiId1==taxiId2 and time1.hour==time2.hour:
                v=calDistance(lon1, lat1, lon2, lat2)/((time2-time1).seconds)
#                 print(calDistance(lon1, lat1, lon2, lat2))
#                 print((time2-time1).seconds)
#                 print("seid="+str(sectionId1)+"hourid="+str(time1.hour-firstTime.hour)+"dayId="+str((time1-firstTime).days))
                speed[sectionId1][time1.hour-firstTime.hour][(time1-firstTime).days].append(v)
            taxiId1=taxiId2;lat1=lat2;lon1=lon2;time1=time2
#             print(sectionId1)
            sectionId1=calSectionId(lon1, lat1,minLon, lonLen, minLat, latLen, n)
    
    res=[]
    for i in range(n*n):
        li=[]
        res.append(li)
        for j in range(numOfHours):
            temp=[]
            for k in range(numOfDays):
                temp.append(numpy.mean(speed[i][j][k]))
            if math.isnan(temp[0]):
                li.append(defaultVel)
            else:
                li.append(numpy.mean(temp))
            
    return res