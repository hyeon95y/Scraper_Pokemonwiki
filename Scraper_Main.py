#-*- coding: utf-8 -*-
'''
Created on 2017. 4. 19.

@author: HyeonWoo
'''

#csv
import CSV_Pokepagos as userCsv

#selenium
from selenium import webdriver
import BeautifulSoup_Pokepagos as userParser
from CSV_Pokepagos import show_pokemon_data

if __name__ == '__main__':
    pass


#1. 기존 파일 오픈
tempFile = userCsv.read_pokemon_data()
#show_pokemon_data(tempFile)


#2. geckodriver 로드
driver = webdriver.Firefox(executable_path =r"/Library/Frameworks/Python.framework/Versions/3.5/bin/geckodriver")



#3. 파싱
#앞쪽이 전국도감 넘버
'''
pokemon_name = tempFile[130][4]
pokemon_name = '갸라도스'
userParser.parser(tempFile,pokemon_name, driver)
'''

#(1,5)로 지정하면 1,2,3,4 실행됨
for index in range(192, 830):
    pokemon_name = tempFile[index][4]
    try : 
        userParser.parser(index, tempFile, pokemon_name, driver)
        #파일 덮어쓰기
        userCsv.write_pokemon_data(tempFile)
    except : 
        print('#URL오류 : ',pokemon_name)


