import json                         #json 저장용
import requests                     #크롤링 사이트 리퀘스트
from bs4 import BeautifulSoup       #데이터 크롤링
import time                         #시간 딜레이
import datetime						#시간확인
import pytz                         #파이썬 타임존

#기본 저장 경로 지정
data_path='/data/storage/'

#아카라이브 핫딜 채널 데이터 크롤링
def get_data():
    url = 'https://arca.live/b/hotdeal'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    #vrow hybrid 클래스 내 데이터 크롤링
    #필요한 데이터 목록
    #썸네일 : vrow-preview
    #판매처 : deal-store
    #품목 : kind
    #글 제목 : data
    #가격 : price
    #배송료 : delivery
    #원글 주소 : link
    vrow_elements = soup.find_all('div', class_='vrow hybrid')
    for element in vrow_elements:
        #preview_img = element.find('div', class_='vrow-preview').find('img')['src']
        market = element.find('span', class_='deal-store').text.replace('\n', '')
        kind = element.find('a', class_='badge').text.replace('\n', '')
        price = element.find('span', class_='deal-price').text.replace('\n', '')
        delivery = element.find('span', class_='deal-delivery').text.replace('\n', '')
        title_element = element.find('a', class_='title')
        data = title_element.text.replace('\n', '')
        link = "arca.live" + title_element['href']
        #results.append({'preview_img': preview_img, 'market': market, 'kind': kind, 'data': data, 'price': price, 'delivery': delivery, 'link': link, })
        results.append({'market': market, 'kind': kind, 'data': data, 'price': price, 'delivery': delivery, 'link': link, })
    return results

#데이터 크롤링 후 저장
#def save_to_file(filename, data):
#    with open(filename, 'w', encoding='utf-8') as f:
#        json.dump(data, f, ensure_ascii=False)
def save_to_file(filename, data):
    filename = data_path + filename
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


#저장된 데이터 불러오기
def load_from_file(filename):
    filename = data_path + filename
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


#데이터 비교 후 값 검증하기
def compare_and_save_new_data(origin_data, temp_data):
    origin_links = [item['link'] for item in origin_data]
    new_data = [item for item in temp_data if item['link'] not in origin_links]
    if new_data:
        save_to_file('new_data.json', new_data)
        save_to_file('origin_data.json', temp_data)
        save_to_file('temp_data.json', [])


#가져온 데이터를 origin_data.json에 저장하기
origin_data = get_data()
save_to_file('origin_data.json', origin_data)


#1시간 마다 반복
#while True:
#    time.sleep(3600) # wait for 10 minutes
#
#    temp_data = get_data()
#    save_to_file('temp_data.json', temp_data)
#
#    compare_and_save_new_data(origin_data, temp_data)

#매정시마다 반복 UTC
#while True:
#    now = datetime.datetime.now()
#    wait_time = 3600 - (now.minute * 60 + now.second)
#    time.sleep(wait_time)
#
#    temp_data = get_data()
#    save_to_file('temp_data.json', temp_data)
#
#    compare_and_save_new_data(origin_data, temp_data)

#매정시마다 반복 KST
while True:
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(tz)
    wait_time = 3600 - (now.minute * 60 + now.second)
    time.sleep(wait_time)

    temp_data = get_data()
    save_to_file('temp_data.json', temp_data)

    compare_and_save_new_data(origin_data, temp_data)
