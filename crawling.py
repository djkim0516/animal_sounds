#-*- coding: cp949 -*-
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image,ImageDraw,ImageFont
import psycopg2
import argparse
import math

'''
1. 이미지 저장 0
2. 저장한 이미지에 저작권 적어주기 0
3. 데이터 베이스에 저장할수있게 코드화 0
4. 서버에서 바로 실행할수있게 세팅하기
DELETE FROM public.blog_animal_map WHERE id BETWEEN 382226 AND 383755;
DELETE FROM public.blog_animal_map;
DELETE FROM public.blog_animal_sub_file ;
DELETE FROM blog_animal_sub_file ;
DELETE FROM blog_animal_map;

'''
## 시작 페이지, 마지막 페이지, 디비 아이디, 비밀번호, 이미지 폴더
parse = argparse.ArgumentParser(description="테스트입니다.")
parse.add_argument('--startpage',required=False, default=1, help="시작 페이지 수")
parse.add_argument('--id',required=False, default='postgres',help="비디 아이디")
parse.add_argument('--passward',required=False,default='password', help="비디 비밀번호")
parse.add_argument('--folder',required=False, default='./', help="이미지 폴더 위치")

def image_save(x,y):

    urllib.request.urlretrieve(x,"./"+args.folder+y+".jpg")

def modify(x,y):
    target_image=Image.open("./"+args.folder+x+".jpg")
    width, height = target_image.size
    draw = ImageDraw.Draw(target_image)
    font = ImageFont.truetype("gulim.ttf",size=30)
    draw.text((0,0),y,font=font,fill='blue')
    target_image.save("./"+args.folder+x+".jpg")

args= parse.parse_args()

print(args.startpage)
print(args.id)
print(args.passward)
print(args.folder)
html = urlopen("https://www.naturing.net/o/thumbnail?observation_name=&order_code=mammals%2Cbirds%2Creptilia%2Camphibians%2Cbugs&habitat_code=&area=&help_name_yn=N&match_case=N&observe_date1=&observe_date2=&create_date1=&create_date2=&obs_filter=0&follow_yn=&photo_yn=Y&type=&draft_yn=&lat1=&lng1=&lat2=&lng2=&page=0")
bsObject = BeautifulSoup(html, "html.parser")
last_page=float(bsObject.find("div",{"id":"paging"}).get("data-total-count"))/float(bsObject.find("div",{"id":"paging"}).get("data-page-size"))
print(math.ceil(last_page))

for page in range(math.ceil(last_page)):
    print(page)
    # 메인 페이지 접속
    html = urlopen("https://www.naturing.net/o/thumbnail?observation_name=&order_code=mammals%2Cbirds%2Creptilia%2Camphibians%2Cbugs&habitat_code=&area=&help_name_yn=N&match_case=N&observe_date1=&observe_date2=&create_date1=&create_date2=&obs_filter=0&follow_yn=&photo_yn=Y&type=&draft_yn=&lat1=&lng1=&lat2=&lng2=&page="+str(page))
    bsObject = BeautifulSoup(html, "html.parser")

    #print(bsObject)
    # 상세 페이지 접속
    for link in bsObject.find_all("a", {"class":"observationView b-itemlist__item__link observation-item__link"}):
        # print("https://www.naturing.net/o/"+link.get('href'))
        html_sub = urlopen("https://www.naturing.net/o/" + link.get('href'))
        bsObject_sub = BeautifulSoup(html_sub, "html.parser")
        try:
            id = link.get('href')
            print(id)  # id
            Latitude=bsObject_sub.find("div", {"id": "map"}).get("data-lat")
            Latitude=("{:.7f}".format(float(Latitude)))
            print(Latitude)  # 좌표 lat
            Longitude=bsObject_sub.find("div", {"id": "map"}).get("data-lng")
            Longitude = ("{:.7f}".format(float(Longitude)))
            print(Longitude)  # 좌표 lng
            title=bsObject_sub.find("meta", {"property": "og:title"}).get("content")
            print(title)  # 한글 이름.
            try:
                print(bsObject_sub.find_all("a", {"class": "obsinfo__link b-btn"})[1].get("href").split("https://en.wikipedia.org/wiki/")[1])  # 영어 이름. 아직 못하는 중...
            except IndexError:
                pass
            #print(bsObject_sub.find("meta", {"property": "og:image"}).get("content"))  # 사진 하나
            image_save(bsObject_sub.find("meta", {"property": "og:image"}).get("content"),id)

            animalclass=bsObject_sub.find("div", {"id": "map"}).get("data-order_code")
            if animalclass=='bugs': #곤충
                animalclass="i"
            elif animalclass=='birds': #새
                animalclass="b"
            elif animalclass=='mammals': #포유류
                animalclass="m"
            elif animalclass=='amphibians': #양서류
                animalclass="a"
            elif animalclass=='reptilia': #파충류
                animalclass="r"

            print(animalclass)  # 동물 분류 종류

            print(" ".join(bsObject_sub.find("div", {"class": "obsinfo__item-content"}).text.split()))  # 주소
            address = " ".join(bsObject_sub.find("div", {"class": "obsinfo__item-content"}).text.split())
            addresssub = address.split(" ")[0]
            print(addresssub)
            if addresssub=='서울':
                addresssub="a"
            elif addresssub=='경기'or addresssub=='경기도': #새
                addresssub="b"
            elif addresssub=='강원': #포유류
                addresssub="c"
            elif addresssub=='충남' or addresssub=='충청남도': #양서류
                addresssub="d"
            elif addresssub=='충북' or addresssub=='충청북도': #파충류
                addresssub="e"
            elif addresssub=='경남' or addresssub=='경상남도': #새
                addresssub="f"
            elif addresssub=='경북' or addresssub=='경상북도': #포유류
                addresssub="g"
            elif addresssub=='전남' or addresssub=='전라남도' or addresssub=='광주': #양서류
                addresssub="h"
            elif addresssub=='전북' or  addresssub == '전라북도': #파충류
                addresssub="i"
            elif addresssub=='제주특별자치도': #새
                addresssub="j"
            elif addresssub=='세종특별자치시': #포유류
                addresssub="l"
            elif addresssub=='인천광역시' or addresssub=='인천': #양서류
                addresssub="m"
            elif addresssub=='대전': #파충류
                addresssub="n"
            elif addresssub=='울산': #새
                addresssub="o"
            elif addresssub=='대구': #포유류
                addresssub="p"
            elif addresssub=='부산' or addresssub == '부산광역시': #양서류
                addresssub="q"
            observed_date=bsObject_sub.find_all("div", {"class": "obsinfo__item-content"})[3].text.strip()

            created_date=bsObject_sub.find("p", {"class": "obsauthor__post-time"}).text.strip()
            created_date = created_date.replace("년 ", "-").replace("월 ", "-").split("일 ")[0]
            #print(created_date)  # 등록 날짜
            observed_date = observed_date.replace("년 ", "-").replace("월 ", "-").split("일 ")[0]
            if observed_date == '0000-0-0':
                observed_date=created_date

            #print(observed_date)  # 관찰 날짜


            writer=bsObject_sub.find("p", {"class": "obsauthor__name"}).text.strip()
            #print(writer)  # 등록자
            cc="(C) " + bsObject_sub.find("p", {"class": "obsauthor__name"}).text.strip() + " at 네이처링"
            modify(id,cc)


            imagefile="/img/"+id+".jpg"
            soundfile="sound/170605_세종시_금개구리1.wav"
            file = 'subsound/subFile0.wav'
            start_point = "6.4319340"
            end_point = "16.3211867"

            # 데이터 베이스에 저장
            conn_string = "host='localhost' dbname ='django_test' user='"+args.id+"' password='"+args.passward+"'"
            conn = psycopg2.connect(conn_string)
            cur= conn.cursor()
            cur.execute('select id from blog_animal_map where id='+id+';')
            result= cur.fetchall()
            if result==[]:
                print('insert into blog_animal_map(id, writer , animalclass, title, "Latitude", "Longitude", address, imagefile, soundfile, observed_date, created_date ) values ('+id+",'"+writer+"','"+animalclass+"','"+title+"','"+Latitude+"','"+Longitude+"','"+addresssub+"','"+imagefile+"','"+soundfile+"','"+observed_date+"','"+created_date+"');")
                cur.execute('insert into blog_animal_map(id, writer , animalclass, title, "Latitude", "Longitude", address, imagefile, soundfile, observed_date, created_date ) values ('+id+",'"+writer+"','"+animalclass+"','"+title+"','"+Latitude+"','"+Longitude+"','"+addresssub+"','"+imagefile+"','"+soundfile+"','"+observed_date+"','"+created_date+"');")
                cur.execute('insert into blog_animal_sub_file(id,file,start_point,end_point,"Animal_map_id") values ('+id+",'"+file+"','"+start_point+"','"+end_point+"','"+id+"');")
                conn.commit()

        except AttributeError:
            pass
    break


