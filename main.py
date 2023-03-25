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

YEAR = "2019"

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
    
    
    ## 1着〜3着までの馬番の人気を取得
    NUM_RANK_DICT = {}
    RANK_1_TO_3_LIST = []
    for row in race_info.itertuples():
        try:
            if row[11] != "NaN":
                NUM_RANK_DICT[int(row[3])] = int(row[11])
                if len(RANK_1_TO_3_LIST) < 3:
                    RANK_1_TO_3_LIST.append(row[11])
        except:
            pass
    
    result_safe = True
    for rk in RANK_1_TO_3_LIST:
        if rk > 4:
            result_safe = False
            break
    
    odds = pd.concat([odds_1,odds_2])
    
    # print(race_info)
    fileName = f"all_data/{YEAR}/{CODE_LIST[course_code]}/races/{str(race_id)}_{race_name}.csv"
    race_info.to_csv(fileName, index=False)
    # print(odds)
    fileName = f"all_data/{YEAR}/{CODE_LIST[course_code]}/odds/{str(race_id)}_{race_name}.csv"
    odds.to_csv(fileName, index=False)
    
    
    
    # 3連単の馬順のみを取得
    # settingCount = 0
    # if str(odds.iat[5,0]) != "三連複":
    #     settingCount = 6
    # else:
    #     settingCount = 5
    # three_part_unit = str(odds.iat[settingCount,1])
    # three_part_unit_odds = int(odds.iat[settingCount,2])
    # three_part_unit = three_part_unit.split("→")
    # print(f"[[ {result_safe} ]] {RANK_1_TO_3_LIST}  >>> ODDS : {three_part_unit_odds}円")
    # return result_safe,three_part_unit_odds,race_name
    
    # 三連複の馬のみ取得
    # three_part_unit = str(odds.iat[6,1])
    # three_part_unit_odds = int(odds.iat[6,2])
    # three_part_unit = three_part_unit.split("-")
    # print(f"[[ {result_safe} ]] {RANK_1_TO_3_LIST}  >>> ODDS : {three_part_unit_odds}円")
    # return result_safe,three_part_unit_odds,race_name
    # race_info.to_csv('/Users/sirius1000/keiba/scraping/csv/sample_pandas_normal2.csv')
    # odds.to_csv('/Users/sirius1000/keiba/scraping/csv/sample_pandas_normal.csv')

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
    for index, ril in enumerate(race_id_list):
        try:
            print(f"--- {index} / {len(race_id_list)} ---")
            year,held_count,course_code,day,race_num = parse_id(ril)
            
            url = "https://db.netkeiba.com/race/" + ril
            race_name = get_race_name(url)
            print("========")
            count += 1
            get_race(ril)
        except:
            pass
        # result_safe,three_part_unit_odds,race_name = get_race(ril)
        # if race_name not in raceCount_hist:
        #     raceCount_hist[race_name] = 0
        # raceCount_hist[race_name] += 1
        # if result_safe:
        #     if race_name not in raceName_hist:
        #         raceName_hist[race_name] = 0
        #     raceName_hist[race_name] += 1
        #     get_odds += three_part_unit_odds
        # print(f"""
        # count : {count}回 , 獲得金額 : {get_odds}円 , 収支 : {get_odds - count*PAY_NUM} 割合 : {get_odds / (get_odds - count*PAY_NUM) * 100}
        # """)
        
            
                
        # except:
        #     pass
    
    # ALL_PAYED = PAY_NUM * count
    # print(f"""
    #     count : {count}回 , 獲得金額 : {get_odds}円 , 収支 : {get_odds - ALL_PAYED}
    #     """)

    # with open("dct.csv","w") as f:
    #     writer = csv.writer(f)
    #     for k, v in raceName_hist.items():
    #         writer.writerow([k,v])
            
    # with open("dctAll.csv","w") as f:
    #     writer = csv.writer(f)
    #     for k, v in raceCount_hist.items():
    #         writer.writerow([k,v])
    
    
if __name__ == "__main__":
    main()