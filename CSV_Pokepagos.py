#-*- coding: utf-8 -*-
'''
Created on 2017. 4. 19.

@author: HyeonWoo
'''


import csv
import math
import codecs


how_many_index = 849;
how_many_properties = 28;

def read_pokemon_data():
    #첫번째가 col 두번째가 row
    pokemon_data = [[0]*how_many_properties for row in range(how_many_index)]

    
    f = open('/Users/HyeonWoo/Google 드라이브/Pokepagos/pokemon number(csv).csv', 'r', encoding="utf-8")  
    csvReader = csv.reader(f)    #reader로 파일을 읽는다. 
    
    #i는 리스트 j는 인덱스(col) i는 인덱스(row)
    for index, i in enumerate(csvReader):
        for j in range (0,how_many_properties):
            pokemon_data[index][j] = i[j]
        
    return pokemon_data
    f.close()
    
def show_pokemon_data(pokemon_data):
    
    for i in range (0, how_many_index):
        tempString = ''
        for j in range (0, how_many_properties):
            tempString += (pokemon_data[i][j] + ',')
        print(tempString)
            
def write_pokemon_data(pokemon_data):
    filepath = '/Users/HyeonWoo/Google 드라이브/Pokepagos/pokemon number(csv).csv'
    f = open(filepath, 'w', newline='', encoding="utf-8")
    csvWriter = csv.writer(f)
    
    for index, i in enumerate(pokemon_data):
        #champ_datad[0]은 비어있는 라인. (처음에 챔프넘버 = 인덱스 넘버로 쓰고싶다고 찡찡거리면서 첫칸 비우고 받아왔기 때문) 
        #즉 비어있는 라인 문제를 해결하기 위해서는 write할때 첫줄부터 차있는 새 array를 만들어서 써야 한다. 
        csvWriter.writerow(pokemon_data[index])
    f.close()
            
            
            