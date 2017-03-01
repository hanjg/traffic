'''
Created on 2017年2月8日

@author: hjg
'''
from _operator import index

from numpy import array, ndarray





import numpy
import pandas
from pandas.core.frame import DataFrame


# df=pandas.read_csv("B:\\文档资料\\大数据竞赛\\智慧中国杯\\车速预测\\交通赛数据_上\\20140803_train.txt", 
df=pandas.read_csv("A:\\tra.txt",
                    header=None, 
                    names=["taxiId","lat","lon","busy","time"], 
                    dtype={"taxiId":numpy.int16,"lat":numpy.double,"lon":numpy.double,
                                  "busy":numpy.int8,"time":numpy.str},
                    )
zero=[];one=[];two=[];three=[];four=[]
count=0
for row in df.itertuples(index=False):
    zero.append(row[0])
    one.append(row[1])
    two.append(row[2])
    three.append(row[3])
    four.append(row[4])
    count+=1
    if row[0]>10 : break
df2=DataFrame({'0':zero,'1':one,'2':two,'3':three,'4':four},
              index=list(range(count)))
df2.to_csv('text.txt',index=False,header=None)
