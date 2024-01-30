import requests
import xmltodict
import os
import csv
import datetime
import time
import random

from user_agent import generate_navigator, generate_user_agent
from datetime import date

from pytimekr import pytimekr

col = ["날짜", "노선ID","정류장 ID","정류장 명", "버스 구분", "혼잡도", "평일/금요일/공휴일(주말)", "이전 휴일 수", "이후 휴일 수"]

_now = datetime.datetime.now()
_filename = "cache/Holiday " + _now.strftime("%Y-%m") + ".dat"

#버스 맵핑 추가
bus_id_file = open('bus_id_map.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(bus_id_file)

bus_id_map = {}
for line in rdr :
    bus_id_map[(line[1])]=int(line[0])
    
    
def currentmillisec():
    return round(time.time()*1000)

# OPEN API REQUEST
def api_request():

    t1 = currentmillisec()

    read_routeID()

    t2 = currentmillisec()
    #print("reading route ID : " + str(t2 - t1))

    api_url = "http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll"
    filename = time.strftime('%Y%m%d%H%M_')+'.csv'
    f = open(filename,'w',newline='') 
    wr = csv.writer(f)
    for i in route_id:
        time.sleep(1)
        params = {
            "serviceKey": service_key,
            "busRouteId": i
        }
        t_req = currentmillisec() 
        hdr = {'User-Agent' : generate_user_agent(os='win', device_type='desktop')}
        response = requests.get(api_url, params=params, headers=hdr)
        t_res = currentmillisec()
        save_data(response, i, wr)
        t_sav = currentmillisec()
    
    t_end = currentmillisec()
    
    #print("requesting time : " + str(t_res - t_req))
    #print("writing time : "+ str(t_sav - t_res))
    #print("total req and write time : "+str(t_end-t2))
    print("["+str(datetime.datetime.now())+"] data scraping complete!")
    print("total time : "+str(t_end - t1)+"\n")
    
    f.close()

def getDate(str):
    _str = str.split(' ')
    
    date_str = _str[0].split('-')

    _year = int(date_str[0])
    _month = int(date_str[1].lstrip("0"))
    _day = int(date_str[2])

    _date = date(_year,_month,_day)

    return _date

def getHolidayValue(_date):
    _value = -1

    # 해당 파일이 있는지 확인
    try:
        open(_filename, 'r')
    except FileNotFoundError:
        os.mkdir('cache')
        saveHoliday(_now.year - 1)
        saveHoliday(_now.year)
        saveHoliday(_now.year + 1)

    weekday = _date.weekday()

    # 공휴일
    with open(_filename, 'r') as file:
        for day in file:
            if day == _date.strftime('%Y%m%d'):
                return 2
    # 월/화/수/목
    if weekday < 4:
        return 0
    # 금
    elif weekday == 4:
        return 1
    # 토/일
    elif weekday >= 5:
        return 2
    return _value

def prev_holiday(mkTm) :
    cnt = 0
    _date = mkTm
    _date = _date + datetime.timedelta(days=-1)

    while getHolidayValue(_date) == 2:
        cnt+=1
        _date = _date + datetime.timedelta(days=-1)
    return cnt

def next_holiday(mkTm) :
    cnt = 0
    _date = mkTm
    _date = _date + datetime.timedelta(days=1)

    while getHolidayValue(_date) == 2:
        cnt+=1
        _date = _date + datetime.timedelta(days=1)
    return cnt

# SAVE XML DATA
def save_data(response, route_id, wr):
    data = xmltodict.parse(response.text)

    _flag = False
    try:
        for item in data['ServiceResult']['msgBody']['itemList']:
            #차고대기이거나 특수한 경우 (자료에 잡히지 않아야하는 차량)
            if item['rerdie_Div1'] == "0":
                continue

            if _flag == False:
                date = item['mkTm']
                _date = getDate(date)
                if _date.year < 2024 :
                    return
                prev = prev_holiday(_date)
                next = next_holiday(_date)
                isHoliday = getHolidayValue(_date)
                _flag = True

            _time = ""
            _time = date.split(' ')[1]
            _time = _time.split(':')
            output_time = _time[0] + _time[1]
            output_route_id = bus_id_map[route_id]
            #print(item)
            wr.writerow([_date.month, output_time , output_route_id, item['stId'], item['reride_Num1'], isHoliday,prev,next])
    except:
        print(data)

def read_routeID():
    _f = open('route.csv', 'r',encoding='utf-8-sig')
    rd = csv.reader(_f)

    for i in rd:
        route_id.append("".join(i))

    random.shuffle(route_id)    
    _f.close()

#Save holiday data
def saveHoliday(year):
    api_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    params = {
        'solYear': year,
        'numOfRows': 30,
        'ServiceKey': service_key
    }
    while True:
        response = requests.get(api_url, params=params)
        data = xmltodict.parse(response.text)
        try:
            #오류 데이터 반환시 'response' 키가 없음. 그래서 정상인 경우에만 출력 가능.
            print(data['response']['body']['items']['item'])
            break
        except KeyError:
            continue


    with open(_filename, 'a') as file:
        for item in data['response']['body']['items']['item']:
            file.write(item['locdate'] + '\n')

    
service_key = "qyyrUy+iRL8fFwscuzSxurpdhJsQNqQhRzdYTMhlz4WjkuIZAPpjSM2kIggooumn9c53PItPbAX9xND5n0ni9g=="
route_id = [] #버스 노선

api_request()

