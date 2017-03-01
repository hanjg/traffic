'''
Created on 2017年2月7日

@author: hjg
'''
import math
import os


def eachFile(catalog):
    '''返回目录下的所有文件名的列表'''
    res=[]
    files =  os.listdir(catalog)
    for fileName in files:
        child = os.path.join('%s/%s' % (catalog, fileName))
        res.append(child)
    return res
def calDistance(lon1,lat1,lon2,lat2):
    '''根据经度和纬度计算两点的直线距离'''
    dx = lon1 - lon2
    dy = lat1 - lat2
    b = (lat1 + lat2) / 2.0;
    Lx = (dx/57.2958) * 6371004.0* math.cos(b/57.2958)
    Ly = 6371004.0 * (dy/57.2958)
    return math.sqrt(Lx * Lx + Ly * Ly)

def calSectionId(lon,lat,minLon, lonLen, minLat, latLen, n):
    '''根据经纬度计算地区号'''
    x=int((lon-minLon)/lonLen)
    y=int((lat-minLat)/latLen)
    return int(x*n+y)

