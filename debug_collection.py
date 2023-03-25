import sys
sys.path.append("lib.bs4")
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import urllib.request
import re
import csv


CODE_LIST = {
    "01" : "札幌",
    "02" : "函館",
    "03" : "福島",
    "04" : "新潟",
    "05" : "東京",
    "06" : "中山",
    "07" : "中京",
    "08" : "京都",
    "09" : "阪神",
    "10" : "小倉"
}

YEAR = "2022"

def parse_id(race_id):
    year = race_id[:4]
    course_code = race_id[4:6]
    held_count = race_id[6:8]
    day = race_id[8:10]
    race_num = race_id[10:12]
    
    print(f"{year}年 {held_count}回 {CODE_LIST[course_code]} {day}日目 第{race_num}レース")
    return year,held_count,course_code,day,race_num

def get_race(race_id):
    year,held_count,course_code,day,race_num = parse_id(race_id)
    url = "https://db.netkeiba.com/race/" + race_id
    print(url)
    race_name = get_race_name(url)
    race_info = pd.read_html(url)[0]
    odds_1 = pd.read_html(url)[1]
    odds_2 = pd.read_html(url)[2]
    print(pd.read_html(url)[8])
    
def get_baba(raceId):
    Base = 'https://race.netkeiba.com/race/result.html?race_id='  # レース結果のURL
    url = Base + raceId  # レース結果のURL
    print('\n' + raceId)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    raceName = soup.find(class_="RaceName")
    print(raceName)
    # レース情報(芝・ダート・障害・距離)取得
    raceData = soup.find(class_="RaceData01")
    # 芝・ダート・障害/距離取得
    baba_distance = raceData.span.text.strip()
    # 芝・ダート・障害 取得
    baba = baba_distance[0]
    print(baba)

def get_race_name(race_url):
    try:
        html = urllib.request.urlopen(race_url).read()
        root = BeautifulSoup(html, 'lxml')
        race_dict = {}
        race_dict['race_title'] = root.find('dl', class_='racedata fc').dd.h1.contents[0]
        print(race_dict)
        return race_dict['race_title']
    except:
        return "ERROR"
    
    
def gen_race_id():
    race_id_list = []
    for place in range(1, 11, 1):
        for kai in range(1, 6, 1):
            for day in range(1, 9, 1):
                for r in range(1, 13, 1):
                    race_id = (
                        YEAR
                        + str(place).zfill(2)
                        + str(kai).zfill(2)
                        + str(day).zfill(2)
                        + str(r).zfill(2)
                    )
                    race_id_list.append(race_id)
    return race_id_list

def main():
    PAY_NUM = 600
    
    race_id_list = gen_race_id()
    count = 0
    get_odds = 0
    pay = 0
    raceName_hist = {}
    raceCount_hist = {}
    year,held_count,course_code,day,race_num = parse_id(str(202207020611))
    
    url = "https://db.netkeiba.com/race/" + str(202207020611)
    # get_race(str(202207020611))
    get_baba(str(202207020611))
if __name__ == "__main__":
    main()