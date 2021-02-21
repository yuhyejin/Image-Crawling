# 내장함수
import os
import errno
from urllib.request import urlopen
# 명령행 파싱 모듈 argparse 모듈 사용
import argparse
# request => 요청하는거를 웹에 요청한 결과값을 얻어올수 있는 모듈
import requests as req
import os
import errno
# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup

raw = req.get("https://www.melon.com/chart/day/index.htm", headers={"User-Agent": "XY"})
clips = BeautifulSoup(raw.text, "html.parser")
songlist = clips.select("div.wrap_song_info")

ranking = []

def main():
    url_info = "https://www.google.co.kr/search?"

    for i in songlist:
        title = i.select("div > span > a")
        if len(title) == 0:
            continue
        tmp = {}
        tmp['title'] = title[0].text
        tmp['singer'] = title[1].text
        ranking.append(tmp)

    for i in ranking:
        fileN = "C:/melon"
        name = i['title'] + "_" + i['singer']
        name_n =name.replace("/","").replace(":","").replace("\"","")
        file = fileN + "/" + name_n + "/"

        try:
            os.makedirs(file)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass

        params = {
            "q" : name_n,
            "tbm":"isch"
        }
        #url 요청 파싱값
        html_object = req.get(url_info,params) #html_object html source 값

        if html_object.status_code == 200:
            #페이지 status_code 가 200 일때 2XX 는 성공을 이야기함
            bs_object = BeautifulSoup(html_object.text,"html.parser")
            #인스턴스 생성
            img_data = bs_object.find_all("img")
            #인스턴스의 find_all 이라는 함수에 img 태그가 있으면 img_data에 넣어줌

            for i in enumerate(img_data[1:11]):
                #딕셔너리를 순서대로 넣어줌
                t = urlopen(i[1].attrs['src']).read()

                filename = file + name_n + str(i[0]+1)+'.jpg'

                with open(filename,"wb") as f:

                    f.write(t)
                print("Img Save Success")

if __name__ == "__main__":
    main()
