import csv
import os
import pandas as pd
import copy
import matplotlib.pyplot as plt
import sys
sys.path.append("lib.bs4")
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import urllib.request
import re
import csv


def read_file(csv_file):
    # with open(csv_file, newline="") as f:
    #     reader = csv.reader(f, delimiter=',', quotechar='"')
    #     for row in reader:
    #         for col in row:
    #             print(col,end=" ")
    #         print()
    
    df = pd.read_csv(csv_file)
    return df

def read_Data():
    year = 2022
    race_place = "中京"
    races_data = {}
    for year in range(2013,2023):
    
        dir_path = f"./all_data/{str(year)}/{str(race_place)}/races"
        
        file_names = os.listdir(dir_path)
        
        for fileName in file_names:
            # print(f"fileName : {fileName}")
            race_Lists = ["CBC","高松宮","浜松"]
            if "CBC" in fileName or "高松宮" in fileName or "浜松" in fileName :
                print(f"fileName : {fileName}")
                df = read_file(f"{dir_path}/{fileName}")
                races_data[fileName] = df
    # print(races_data)
    return races_data

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
    # 馬場状態取得
    if soup.find(class_="Item04"):
        babaCondition = soup.find(
            class_="Item04").text[5:]
    elif soup.find(class_="Item03"):
        babaCondition = soup.find(
            class_="Item03").text[5:]
    else:
        pass
    print(babaCondition)
    return babaCondition

def gen_graph(data):
    # 辞書をpandasのデータフレームに変換する
    df = pd.DataFrame.from_dict(data, orient='index')

    # 同じキーがある場合には、値を足し合わせる
    df = df.groupby(df.columns, axis=1).sum()

    # 棒グラフを作成する
    ax = df.plot(kind='bar')

    # 軸ラベルを設定する
    plt.xlabel('zyuni +1 shite')
    plt.ylabel('hindo')

    
    
    # ファイル名を指定する
    file_name = 'bar_chart.png'

    # 既に同じ名前のファイルがある場合は、ファイル名を変更する
    if os.path.isfile(file_name):
        i = 1
        while True:
            new_file_name = f'bar_chart_{i}.png'
            if os.path.isfile(new_file_name):
                i += 1
            else:
                file_name = new_file_name
                break

    # 画像として保存する
    plt.savefig(f"out/fig/{file_name}")

def analytics(races_data):
    wakuban_dict = {}
    for i in range(3):
        wakuban_dict[i] = {}
        for k,v in races_data.items():
                goal_arrival = v.loc[i,"枠 番"]
                if goal_arrival not in wakuban_dict[i]:
                    wakuban_dict[i][goal_arrival] = 0
                wakuban_dict[i][goal_arrival] += 1
        sorted_waku = dict(sorted(wakuban_dict[i].items(),key=lambda x: x[1], reverse=True))
        wakuban_dict[i] = copy.deepcopy(sorted_waku)
        
    print(wakuban_dict)
    gen_graph(wakuban_dict)

def main():
    races_data = read_Data()
    analytics(races_data)
    
if __name__ == "__main__":
    main()