'''
Created on 2017年2月7日

@author: hjg
'''

from builtins import str
import datetime

from com.driverSpeed import driverSpeed
from com.myInit import myInit
from com.sectionSpeed import sectionSpeed
from com.svm import train, predict


if __name__ == '__main__':
    startTime=datetime.datetime.now()
    
    numOfDrivers=0#司机数量
    numOfHours=18#每天的时段数量
    numOfDays=0#天数
    n=10#经纬度各分成n段
    minLon=10000#最小经度
    maxLon=0#最大经度
    minLat=10000#最小纬度
    maxLat=0#最大纬度
    lonLen=0#经度区间长度
    latLen=0#纬度区间长度
    defaultVel=5#缺乏数据的默认速度
    #所有数据的初始时刻
    firstTime=datetime.datetime.strptime("2014/8/3 06:00:00","%Y/%m/%d %H:%M:%S")
    
    trainCatalog="data/train"#训练集目录
    trainData=""#训练集文件列表
    preFile="data/pre.txt"#预测集文件
    resultFile="data/result.txt"#结果文件
    tempCatalog='data/temp'#临时文件目录
    tempData=''#临时文件列表
    
    
    #初始化参数
    print('initing:')
    trainData,tempData,numOfDrivers,numOfDays,minLat,maxLat,minLon,maxLon,lonLen,latLen=myInit(
        tempCatalog, trainCatalog, preFile, numOfDrivers, numOfDays, firstTime, minLat, maxLat, minLon, maxLon, n)
    print('inited:'+str(datetime.datetime.now()-startTime))
    time=datetime.datetime.now()
    
    #计算司机平均速度
    print('driverspeeding:')
    ds=driverSpeed(numOfDrivers,numOfHours,numOfDays,tempData,firstTime)
    print('driverspeeded:'+str(datetime.datetime.now()-time))
    time=datetime.datetime.now()
    #计算路段平均速度
    print('sectionspeeding:')
    ss=sectionSpeed(numOfHours,numOfDays,tempData,firstTime,n,minLon, lonLen, minLat, latLen)
    print('sectionspeeded:'+str(datetime.datetime.now()-time))
    time=datetime.datetime.now()
    
    #训练
    print('training:')
    clf=train(ds, ss,tempData,firstTime,n,minLon, lonLen, minLat, latLen,defaultVel)
    print('trained:'+str(datetime.datetime.now()-time))
    time=datetime.datetime.now()
    #预测
    print('predicting:')
    result=predict(ds, ss, clf,preFile,firstTime,n,minLon, lonLen, minLat, latLen,defaultVel)
    print('predicted:'+str(datetime.datetime.now()-time))
    time=datetime.datetime.now()
    
    print('printing:')
    print(result)
    result.to_csv(resultFile,index=False,header=None)
    print('printed:'+str(datetime.datetime.now()-time))
    time=datetime.datetime.now()
    
    endTime=datetime.datetime.now()
    print('runningTime:'+str((endTime-startTime).seconds))
    
    