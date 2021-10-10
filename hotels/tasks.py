# coding:utf-8
# Created by PyCharm.
# Author  : nick（飞虎队工作室）
# Wechat  : cai9503
# Shop    : https://shop.zbj.com/6463852/
# Date    : 2021/10/5
# Time    : 17:56
from celery import shared_task
from hotels.models import Room, Hotel
import datetime
from hotels.helper_wanhao import load_wanhao_rooms


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_rooms():
    return Room.objects.count()


@shared_task
def reroomtype(room_id, name):
    w = Room.objects.get(id=room_id)
    w.roomType = name
    w.save()


@shared_task
def sync_wanhao(room_id):
	#原始数据
    w = Room.objects.get(id=room_id)
    roomType = w.roomType 
    countsBed = w.countsBed 
    countsBreakfirst = w.countsBreakfirst 
    isTwoNightsMore = w.isTwoNightsMore 
    checkInDate = w.checkInDate 
    checkOutDate = w.checkOutDate 
    countsMember = w.countsMember 
    costPrice = w.costPrice 

    #todo 从官网读取数据
    costPrice = 100

    w.costPrice = costPrice
    w.roomSyncTime = datetime.datetime.now()
    w.save()


@shared_task
def sync_hotel():
    hotHotels = ['HGHAJ','BJSJW','BJSJC','BJSFS','BJSRZ','BJSBG','BJSXR','CSXLC','CSXXR','CSXWH','CTUMJ','CTURZ','CTUXR','CTUWH','CKGJW','DLCLC','CANRZ','CANWG','HAKRZ','HGHJW','HGHLC','HRBJW','HRBRZ','HKGDT','HKGKW','HKGXR','HKGWH','JZHRZ','LXAXR','MFMJW','MFMMR','MFMXR','NKGRZ','NNGLC','TAOXR','JNGJW','SYXEB','SYXDB','SYXJW','SYXRZ','SYXXR','SHAEB','SHAJW','SHACP','SHAJF','SHAMJ','SHARZ','SHASZ','SHABG','SHAHL','SHAXR','SHAWH','SZXJW','SZXBA','SZXRZ','SZXXR','SZVWH','TPEWH','TSNRZ','TSNXR','XIYJW','XIYWH','XMNWH','XIYRZ','INCJW','CGOJW','ZUHXR']
    for i in range(7):
        fromDate = (datetime.date.today()+datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        toDate1 = (datetime.date.today()+datetime.timedelta(days=i+1)).strftime("%Y-%m-%d")
        toDate2 = (datetime.date.today()+datetime.timedelta(days=i+2)).strftime("%Y-%m-%d")
        for toDate in [toDate1, toDate2]:
            for numAdultsPerRoom in [1, 2]:
                roomCount = 1
                for hotelno in hotHotels:
                    load_wanhao_rooms(fromDate=fromDate, toDate=toDate, propertyCode=hotelno, roomCount=roomCount, numAdultsPerRoom=numAdultsPerRoom)


