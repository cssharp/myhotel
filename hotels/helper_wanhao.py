import requests
from pyquery import PyQuery as pq
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import os
import time
import datetime
import re
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhotel.settings')  # 设置django环境
import django
from django.utils import timezone
django.setup()
from hotels.models import Room, Hotel

def load(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': 'SECKEY_CID=b8d969e0ebd75bcef6bf55904acd9057f76686ee;',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    }
    r = requests.get('https://www.marriott.com.cn/reservation/availabilitySearch.mi?propertyCode=BJSJW&isSearch=true&currency=&showFullPrice=true', headers=headers)
    logging.warning(r.content)
    


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.warning('log开始 ...',  func.__name__)
        func(*args, **kwargs)
        logging.warning('log结束 ...')
    return wrapper


def load_wanhao_rooms(fromDate='2021-10-13', toDate='2021-10-15', propertyCode='BJSIM', roomCount=1, numAdultsPerRoom=1):
    logging.warning("Step 1) Open Chrome")
    url = 'https://www.marriott.com.cn/reservation/availabilitySearch.mi?propertyCode={2}&isSearch=true&currency=&fromDate={0}&toDate={1}&showFullPrice=true'.format(fromDate, toDate, propertyCode)
    url = 'https://www.marriott.com.cn/search/submitSearch.mi?&recordsPerPage=20&isInternalSearch=true&vsInitialRequest=false&searchType=InCity&collapseAccordian=is-hidden&singleSearch=true&isTransient=true&destinationAddress.longitude=116.4073963&initialRequest=true&flexibleDateSearchRateDisplay=false&isSearch=true&isRateCalendar=false&flexibleDateSearch=false&isHideFlexibleDateCalendar=false&t-start={0}&t-end={1}&lengthOfStay=7&roomCountBox=1+%E5%AE%A2%E6%88%BF&roomCount={3}&numAdultsPerRoom={4}&childrenCount=0&clusterCode=none&destinationAddress.destination=Beijing%2C+China&fromDate={0}&toDate={1}&showFullPrice=true'.format(fromDate, toDate, propertyCode, roomCount, numAdultsPerRoom)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 设置火狐为headless无界面模式
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
    options.add_argument('--disable-gpu')  # 上面代码就是为了将Chrome不弹出界面
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    browser = webdriver.Chrome(options=options, executable_path=".\\tmp\\chromedriver.exe")

    try:
        if os.name != 'nt':
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument('--no-sandbox') #Bypass OS security model, MUST BE THE VERY FIRST OPTION
            chromeOptions.add_argument('--headless')
            chromeOptions.add_argument('--disable-gpu')
            chromeOptions.add_argument('--disable-dev-shm-usage')
            chromeOptions.add_argument('--remote-debugging-port=9222')
            chromeOptions.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
            browser = webdriver.Chrome('/usr/bin/chromedriver', options=chromeOptions)

        logging.warning("Step 2) Navigate to marriott")
        logging.warning(url)
        browser.get(url)
        logging.warning(browser.current_url)
        #logging.warning(browser.execute_script("return document.documentElement.outerHTML"))
        time.sleep(3)

        logging.warning("Step 4) 某个酒店")
        browser.get('https://www.marriott.com.cn/reservation/availabilitySearch.mi?propertyCode={2}&isSearch=true&currency=&fromDate={0}&toDate={1}&showFullPrice=true'.format(fromDate, toDate, propertyCode))
        html = browser.execute_script("return document.documentElement.outerHTML")
        logging.warning(browser.current_url)
        
        v = pq(html)

        #酒店信息
        hotelInfo = {}
        hotelInfo['hotelNo'] = propertyCode
        hotelInfo['name'] = ''
        hotelInfo['addr'] = ''
        hotelInfo['brand'] = '万豪'
        r = r'{"name":"([^\"]+)","address":"([^\"]+)"'
        m = re.findall(r, html)
        if m:
            hotelInfo['name'] = m[0][0]
            hotelInfo['addr'] = m[0][1]
        logging.warning(hotelInfo)

        roomList = []
        #处理房间信息
        def prep_rooms(tab_rooms, roomList, is_youhui):
            for room in tab_rooms:
                roomType = pq(room)("div.m-room-rate-container h3").text()
                logging.warning(roomType)

                sub_rooms = pq(room)(".widget-container")
                for s in sub_rooms:
                    sub_roomType = pq(s)("h3").text()
                    cost = pq(s)("span.t-font-xl").text()
                    if '会员' in sub_roomType:
                        continue
                    logging.warning(sub_roomType)
                    logging.warning(cost)

                    # 床数
                    countsBed = 1
                    r = r'(\d+)\s*张'
                    m = re.findall(r, roomType)
                    if m:
                        countsBed = m[0][0]

                    title = roomType.split(',')[0]

                    roomInfo = {
                        "roomType": roomType,
                        "title": title,
                        "countsBed": countsBed if is_youhui else 0,
                        "countsBreakfirst": numAdultsPerRoom,
                        "isTwoNightsMore": True,
                        "checkInDate": fromDate,
                        "checkOutDate": toDate,
                        "countsMember": numAdultsPerRoom,
                        "costPrice": int(cost.replace(",", "")),
                    }
                    roomList.append(roomInfo)

        #标准房价
        logging.warning("标准房价")
        tab0_rooms = v('#tab0 .room-rate-results')
        prep_rooms(tab0_rooms, roomList, False)


        #优惠套餐
        logging.warning("优惠套餐")
        tab1_rooms = v('#tab1 .room-rate-results')
        prep_rooms(tab1_rooms, roomList, True)


        #todo 同步到数据库
        for roomInfo in roomList:
            logging.warning(roomInfo)

        hotels = Hotel.objects.filter(hotelNo=hotelInfo['hotelNo'])
        if hotels.exists():
            h = hotels.first()
            h.name = hotelInfo['name']
            h.addr = hotelInfo['addr']
            h.save()
            logging.warning("酒店已经存在，需要更新")
            logging.warning(h)
        else:
            h = Hotel.objects.create(hotelNo=hotelInfo['hotelNo'], name=hotelInfo['name'], addr=hotelInfo['addr'], brand=hotelInfo['brand'])

        for roomInfo in roomList:
            rooms = Room.objects.filter(roomType=roomInfo['roomType'], checkInDate=roomInfo['checkInDate'], checkOutDate=roomInfo['checkOutDate'], hotel=h)
            if rooms.exists():
                room = rooms.first()
                room.countsBed=roomInfo['countsBed']
                room.title = roomInfo['title']
                room.countsBreakfirst= roomInfo['countsBreakfirst']
                room.isTwoNightsMore=roomInfo['isTwoNightsMore']
                room.countsMember=roomInfo['countsMember']
                room.costPrice=roomInfo['costPrice']
                room.roomSyncTime=timezone.now()
                room.save()
                logging.warning("房间已经存在，需要更新")
                logging.warning(room)
            else:
                room = Room.objects.create(
                    roomType=roomInfo['roomType'],
                    title=roomInfo['title'],
                    checkInDate=roomInfo['checkInDate'],
                    checkOutDate=roomInfo['checkOutDate'],
                    hotel=h,
                    countsBed=roomInfo['countsBed'],
                    countsBreakfirst= roomInfo['countsBreakfirst'],
                    isTwoNightsMore=roomInfo['isTwoNightsMore'],
                    countsMember=roomInfo['countsMember'],
                    costPrice=roomInfo['costPrice'])

        #submit.click()
        # time.sleep(15)
        # if 'login.taobao.com/member/login.jhtml' in browser.current_url:
        #     logging.error("【{}】用户名或密码错误，请检查一下".format(self.name))
        #     os.system("pause")
        #     sys.exit()
    except Exception as e:
        logging.error(e)
    finally:
        logging.warning("退出browser")
        browser.quit()
    return 1



if __name__ == '__main__':
    hotHotels = ['BJSFS','BJSRZ','BJSBG','BJSXR','HGHAJ','BJSJW','BJSJC','CSXLC','CSXXR','CSXWH','CTUMJ','CTURZ','CTUXR','CTUWH','CKGJW','DLCLC','CANRZ','CANWG','HAKRZ','HGHJW','HGHLC','HRBJW','HRBRZ','HKGDT','HKGKW','HKGXR','HKGWH','JZHRZ','LXAXR','MFMJW','MFMMR','MFMXR','NKGRZ','NNGLC','TAOXR','JNGJW','SYXEB','SYXDB','SYXJW','SYXRZ','SYXXR','SHAEB','SHAJW','SHACP','SHAJF','SHAMJ','SHARZ','SHASZ','SHABG','SHAHL','SHAXR','SHAWH','SZXJW','SZXBA','SZXRZ','SZXXR','SZVWH','TPEWH','TSNRZ','TSNXR','XIYJW','XIYWH','XMNWH','XIYRZ','INCJW','CGOJW','ZUHXR']
    #login('https://www.marriott.com.cn/search/submitSearch.mi?&recordsPerPage=20&isInternalSearch=true&vsInitialRequest=false&searchType=InCity&collapseAccordian=is-hidden&singleSearch=true&isTransient=true&destinationAddress.longitude=116.4073963&initialRequest=true&flexibleDateSearchRateDisplay=false&isSearch=true&isRateCalendar=false&flexibleDateSearch=false&isHideFlexibleDateCalendar=false&t-start=2021-10-14&t-end=2021-10-16&lengthOfStay=7&roomCountBox=1+%E5%AE%A2%E6%88%BF&roomCount=1&numAdultsPerRoom=2&childrenCount=0&clusterCode=none&destinationAddress.destination=Beijing%2C+China&fromDate=2021-10-27&toDate=2021-10-29&showFullPrice=true')
    #load_wanhao_rooms(fromDate='2021-10-13', toDate='2021-10-15', propertyCode='CKGJW')

    for i in range(7):
        fromDate = (datetime.date.today()+datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        toDate1 = (datetime.date.today()+datetime.timedelta(days=i+1)).strftime("%Y-%m-%d")
        toDate2 = (datetime.date.today()+datetime.timedelta(days=i+2)).strftime("%Y-%m-%d")
        for toDate in [toDate1, toDate2]:
            for numAdultsPerRoom in [1, 2]:
                roomCount = 1
                for hotelno in hotHotels:
                    logging.warning("酒店：{}".format(hotelno))
                    load_wanhao_rooms(fromDate=fromDate, toDate=toDate, propertyCode=hotelno, roomCount=roomCount, numAdultsPerRoom=numAdultsPerRoom)


