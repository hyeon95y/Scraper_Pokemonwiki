#-*- coding: utf-8 -*-
'''
Created on 2017. 4. 19.

@author: HyeonWoo
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from test.pickletester import DATA2
import urllib.request, urllib.parse, urllib.error

'''
csv인덱스
0    파이썬인덱스
1    인덱스(파일에서사용) ex. 700-1
2    이미지
3    전국도감번호
4    이름(한국어)
5    이름(일본어)
6    이름(영어)
7    분류
8    특성1
9    특성2
10    숨겨진특성1
11    숨겨진특성2
12    키
13    몸무게
14    포켓몬도감 색깔
15    타입1
16    타입2
17    진화 -2
18    진화 -1
19    진화 +1
20    진화 +2
21    관동(1세대)
22    성도(2세대)
23    호연(3세대)
24    신오(4세대)
25    하나(5세대)
26    칼로스(6세대)
27    알로라(7세대)
'''


def parser(pythonindex, pokemon_data, pokemon_name_korean, driver):
    targetURL = 'http://ko.pokemon.wikia.com/wiki/' + pokemon_name_korean
    driver.get(targetURL)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    champ_name_korean = ''
    #전국도감
    data1 = soup.find("div", {"class":"index"}).find('strong').text.replace(" ", "").replace("\t", "").replace("No.", "")
    print('#전국도감 : ', data1)
    

    #전국도감은 원래 있기 때문에 데이터 안집어넣어도 됨
    
    
    
    #한국어 이름
    data2 = soup.find("div", {"class":"name-ko"}).find('strong').text.replace(" ", "").replace("\t", "")
    print('#이름(한국어) : ', data2)
    champ_name_korean = data2
    pokemon_data[pythonindex][4] = data2
    
    #일본어 이름
    data3 = soup.find("div", {"class":"name"}).find("span", {"lang":"ja"}).text.replace(" ", "").replace("\t", "")
    print('#이름(일본어) : ', data3)
    pokemon_data[pythonindex][5] = data3
    
    #영어 이름
    data4 = soup.find("div", {"class":"name"}).find("span", {"lang":"en"}).text.replace(" ", "").replace("\t", "")
    print('#이름(영어) : ', data4)
    pokemon_data[pythonindex][6] = data4
    
    #테이블
    for index, child in enumerate(soup.find("table", {"class": "body"}).findAll("tr")):
        
        '''
        if index==1 or index==3 or index==4 or index==7 or index==8 or index==12:
            print('********************************************* index : ', index)
            print(child)
        '''
            
        if index==1 :
            #print('********************************************* index : ', index)
            for index, grandchild in enumerate(child.findAll('td')) :
                #print('grandchild index : ', index)
                #print(grandchild)
                if index==0 :
                    for grandindex, grandgrandchild in enumerate(grandchild.findAll('a')) :
                        if grandindex == 0 :
                            data5 = grandgrandchild.get('title').replace(" ", "").replace("\t", "").replace('(타입)', '')
                            print("#타입1 : ", data5)
                            pokemon_data[pythonindex][15] = data5
                        if grandindex == 1 :
                            data6 = grandgrandchild.get('title').replace(" ", "").replace("\t", "").replace('(타입)', '')
                            print("#타입2 : ", data6)
                            pokemon_data[pythonindex][16] = data6
                        
                    
                if index==1 :
                    data7 = grandchild.text.replace("\n", "").replace(" ", "").replace("\t", "")
                    print('#분류 : ', data7)
                    pokemon_data[pythonindex][7] = data7
                    
        if index==3 : 
            #print('********************************************* index : ', index)
            for grandindex, grandchild in enumerate(child.findAll('td')) :
                #print('grandchild index : ', grandindex)
                #print(grandchild)
                #일반특성
                if grandindex==0 :
                    for grandgrandindex, grandgrandchild in enumerate(grandchild.findAll('a')):
                        #print('*******', index)
                        #print(grandgrandchild)
                        #print('*** end of grandgrandchild')
                        if grandgrandindex == 0 :
                            data8 = grandgrandchild.find('span').text.replace(" ", "").replace("\t", "")
                            print('#특성1 : ', data8)
                            pokemon_data[pythonindex][8] = data8
                        if grandgrandindex == 1 :
                            data9 = grandgrandchild.find('span').text.replace(" ", "").replace("\t", "")
                            print('#특성2 : ', data9)
                            pokemon_data[pythonindex][9] = data9
                #숨겨진특성
                if grandindex==1 :
                    #print('grandchild.text')
                    #print('*******', index)
                    try : 
                        data10 = grandchild.find('a').get('title').replace(" ", "").replace("\t", "")
                        print('#숨겨진 특성 : ', data10)
                        pokemon_data[pythonindex][10] = data10
                    except : 
                        print('#숨겨진 특성 : 없음')
                        pokemon_data[pythonindex][10] = ""
        if index==8 : 
            #print('********************************************* index : ', index)
            for grandindex, grandchild in enumerate(child.findAll('td')) :
                #print('grandindex : ', grandindex)
                #print('#도감 html : ', grandchild.text.replace("\n", ""))
                #문자열 중에 숫자를 찾아내는 filter() 함수를 이용함
                space = grandchild.text.replace("\n", "").find(list(filter(str.isdigit, grandchild.text.replace("\n", "")))[0])
                dicname = grandchild.text.replace("\n", "")[:space].replace(" ", "").replace("\t", "").replace("#", "")
                dicnumber = grandchild.text.replace("\n", "")[space:].replace(" ", "").replace("\t", "")
                if dicname=="관동" :
                    print('#관동도감 번호 : ', dicnumber)
                    pokemon_data[pythonindex][21] = dicnumber
                if dicname=="성도" :
                    print('#성도도감 번호 : ', dicnumber)
                    pokemon_data[pythonindex][22] = dicnumber
                if dicname=="호연" :
                    print('#호연도감 번호 : ', dicnumber)
                    pokemon_data[pythonindex][23] = dicnumber
                if dicname=="신오" :
                    print('#신오도감 번호 : ', dicnumber)
                    pokemon_data[pythonindex][24] = dicnumber
                if dicname=="하나" :
                    print('#하나도감 번호 : ', dicnumber)
                    pokemon_data[pythonindex][25] = dicnumber
                if dicname=="칼로스" :
                    print('#칼로스도감 번호 : ', dicnumber)
                    pokemon_data[pythonindex][26] = dicnumber
                if dicname=="알로라" :
                    print('#알로라도감 번호 : ', dicnumber)
                    pokemon_data[pythonindex][27] = dicnumber

               
                
        if index==14 : 
            #print('********************************************* index : ', index)
            for grandindex, grandchild in enumerate(child.findAll('td')) :
                if grandindex==0 :
                    data11 = grandchild.text.replace("\n", "").replace(" ", "").replace("\t", "")
                    print('#키 : ', data11)
                    pokemon_data[pythonindex][12] = data11
                if grandindex==1 : 
                    data12 = grandchild.text.replace("\n", "").replace(" ", "").replace("\t", "")
                    print('#몸무게 : ', data12)
                    pokemon_data[pythonindex][13] = data12
        if index==12 :
            #print('********************************************* index : ', index)
            data13 = child.find('td').text.replace("\n", "").replace(" ", "").replace("\t", "")
            print('#도감 색깔 : ', data13)
            pokemon_data[pythonindex][14] = data13
            
            
                

            
    '''
    타입, 분류 : 1  
    특성, 숨겨진특성 : 3  
    도감번호타이틀 : 7
    도감번호내용 : 8
    키, 몸무게 : 14
    도감색깔 : 12 
    '''
        
    #진화 (진화형이 없을경우 통째로 except로 넘어감)     
    try : 
        
        evolution1 = ''
        evolution2 = ''
        evolution3 = ''
        
        for index, child in enumerate(soup.find("small", text="진화 전").parent.parent.parent.parent.parent.parent.findAll("td")):
            '''
            if index==2 or index==3 or index==7 or index==8 or index==12 or index==13:
                print('****************************** index : ', index)
                print(child)
            '''
            
            
            if index==3 :
                #print('****************************** index : ', index)
                try : 
                    #print('#진화 전 단계 : ', child.find('span').text)
                    evolution1 = child.find('span').text
                except : 
                    print('#진화 전 없음')
            if index==8 :
                #print('****************************** index : ', index)
                try : 
                    #print('#첫번째 진화 : ', child.find('span').text)
                    evolution2 = child.find('span').text
                except :
                    print('#첫번째 진화 없음')
            if index==13 : 
                #print('****************************** index : ', index)
                try : 
                    #print('#두번째 진화 : ', child.find('span').text)
                    evolution3 = child.find('span').text
                except: 
                    print('#두번째 진화 없음')
                    
        #문자열 파싱
        evolution1 = evolution1.replace(" ", "").replace("\t", "")
        evolution2 = evolution2.replace(" ", "").replace("\t", "")
        evolution3 = evolution3.replace(" ", "").replace("\t", "")


        #진화 인덱스 추출
        if evolution1 == champ_name_korean :
            print('#진화 전 단계 : ', evolution1, '0')
            print('#첫번째 진화 : ', evolution2, '+1')
            pokemon_data[pythonindex][19] = evolution2
            print('#두번째 진화 : ', evolution3, '+2')
            pokemon_data[pythonindex][20] = evolution3
            
        if evolution2 == champ_name_korean :
            print('#진화 전 단계 : ', evolution1, '-1')
            pokemon_data[pythonindex][18] = evolution1
            print('#첫번째 진화 : ', evolution2, '0')
            print('#두번째 진화 : ', evolution3, '+1')
            pokemon_data[pythonindex][19] = evolution3
            
        if evolution3 == champ_name_korean :
            print('#진화 전 단계 : ', evolution1, '-2')
            pokemon_data[pythonindex][17] = evolution1
            print('#첫번째 진화 : ', evolution2, '-1')
            pokemon_data[pythonindex][18] = evolution2
            print('#두번째 진화 : ', evolution3, '0')    
                
    except :
        print('#진화형이 없는 포켓몬')
    '''
    1. 3개가 다 있을 경우
    진화전타이틀 : 2
    진화전내용 : 3
    첫번째진화타이틀 : 7
    첫번째진화내용 : 8
    두번째진화타이틀: 12
    두번째진화내용 : 13
    '''
            
    #작은 아이콘 
    print('#작은 이미지')
    for index, child in enumerate(soup.findAll('table', {'class' : ['w-100', 'mb-1', 'p402_hide']})):
        if index==2:
            #print('****************************** index : ', index)
            data14 = child.find('img').get('src')
            print(data14)
            
            #다운로드
            f = urllib.request.urlopen(data14)
            data = f.read()
            with open("/Users/HyeonWoo/Google 드라이브/Pokepagos/img/small/"+pokemon_data[pythonindex][1]+".png", "wb") as code:
                code.write(data)
    #index2에 아이콘 url 들어있음
    
    #큰 아이콘
    print('#큰 이미지')
    data15 = soup.find('img', {'class' : ['lzyPlcHld', 'lzyTrns', 'lzyLoaded']}).get('src')
    print(data15)
    print('\n')
    #다운로드
    f = urllib.request.urlopen(data15)
    data = f.read()
    with open("/Users/HyeonWoo/Google 드라이브/Pokepagos/img/large/"+pokemon_data[pythonindex][1]+".png", "wb") as code:
        code.write(data)
    
    
    #webdriver 종료
    #driver.quit()
