'''
Created on 2017年2月10日

@author: hjg
'''
import numpy
import pandas

from com.utils import eachFile, calSectionId, calDistance
import datetime


def myInit(tempCatalog,trainCatalog,preFile,numOfDrivers,numOfDays,firstTime,minLat,maxLat,minLon,maxLon,n):
    trainData=eachFile(trainCatalog)
    for file in trainData:
        df=pandas.read_csv(file, 
                           header=None, 
                           names=["taxiId","lat","lon","busy","time"], 
                           dtype={"taxiId":numpy.int16,"lat":numpy.float32,"lon":numpy.float32,
                                  "busy":numpy.int8,"time":numpy.str})
        for row in df.itertuples(index=False):
            if row[0]>numOfDrivers: numOfDrivers=row[0]
            if row[1]<minLat: minLat=row[1]
            if row[1]>maxLat: maxLat=row[1]
            if row[2]<minLon: minLon=row[2]
            if row[2]>maxLon: maxLon=row[2]
        numOfDays+=1
        
    lonLen=1.0001*(maxLon-minLon)/n
    latLen=1.0001*(maxLat-minLat)/n
    
    for file in trainData:
        day=0
        calVelAndSec(file, tempCatalog, day, firstTime, minLon, lonLen, minLat, latLen, n)
        day+=1
    
    tempdata=eachFile(tempCatalog)
    
    return trainData,tempdata,numOfDrivers,numOfDays,minLat,maxLat,minLon,maxLon,lonLen,latLen
    
def calVelAndSec(file,tempCatalog,day,firstTime,minLon, lonLen, minLat, latLen, n):
    '''原始数据排序并且增加两列：瞬时速度、地区号，结果写入新的文件"天数temp.txt"'''
    df=pandas.read_csv(file, 
                        header=None, 
                        names=["taxiId","lat","lon","busy","time"], 
                        dtype={"taxiId":numpy.int16,"lat":numpy.float32,"lon":numpy.float32,
                                  "busy":numpy.int8,"time":numpy.str})
        #df按照出租车id，时间点升序排序
    df.sort_values(by=["taxiId","time"], axis=0, ascending=[True,True], inplace=True)
    
    taxiId1=-1
    lat1=0
    lon1=0
    time1=firstTime
    #出租车每点的速度
    vel=[]
    #出租车每点的地区号
    sec=[]
    for row in df.itertuples(index=False):
        taxiId2=row[0]
        lat2=row[1]
        lon2=row[2]
        time2=datetime.datetime.strptime(row[4],"%Y/%m/%d %H:%M:%S")
        if taxiId1==taxiId2:
            t=(time2-time1).seconds
            if t!=0:
                v=calDistance(lon1, lat1, lon2, lat2)/t
                vel.append(v)
            else:
                vel.append(numpy.nan)
        else:
            if taxiId1!=-1:
                vel.append(numpy.nan)
        taxiId1=taxiId2;lat1=lat2;lon1=lon2;time1=time2
        sec.append(calSectionId(lon1, lat1, minLon, lonLen, minLat, latLen, n))
    vel.append(numpy.nan)
    
    df['vel']=vel
    df['sec']=sec
    
    df.to_csv(tempCatalog+'/'+str(day)+'temp.txt',index=False,header=None)
