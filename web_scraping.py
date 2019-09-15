from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

from time import sleep
import random
import xlrd
import xlwt
from xlwt import Workbook
import xlsxwriter
import openpyxl
from openpyxl import Workbook

import re
import mechanize
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import string
#change working directory
os.chdir('/Users/xxxxx/Desktop/dataMining_island')#change to your working dirctory

#login
URL = "https://islands.smp.uq.edu.au/login.php"
driver = webdriver.Chrome(executable_path=r"xxxxxxxxxxxx") #use your unique chromedriver path
driver.get(URL)
email = driver.find_element_by_name("email")
email.clear()
email.send_keys("xxxxxxxxxxx") #use your login email
password = driver.find_element_by_name("word")
password.clear()
password.send_keys("xxxxxxx")   #your account password
driver.find_element_by_name("Sign In").click()

#scrape data for each city
# location = []
# invalid_location = ['Visitor Centre','The Academy','Hofn Field Station','Biruwa Field Station','Mutalau Field Station','Carsten Climate Station','Yakunai Climate Station','Nanu Forest Climate Station','Gido Climate Station']
# num_of_house = []
# soup = BeautifulSoup(driver.page_source, 'html5lib')
# for item in soup.find_all("area"):
#     if item["alt"] not in location and item["alt"] not in invalid_location:
#         location.append(item["alt"])

# for city in location:
#     driver.get("https://islands.smp.uq.edu.au/village.php?"+city)
#     soup2 = BeautifulSoup(driver.page_source, 'html5lib')
#     num = soup2.find_all('div',attrs={'class':'houseid'})
#     num_of_house.append(num[-1].text)
#     print(city)
#     print(num[-1].text)

# df = pd.DataFrame.from_dict({'Cities':location,'number of houses':num_of_house})
# df.to_excel('location.xlsx',header = True, index = False)

#select randomlized people, 27 treatments, 10 replicates
city_list = ['Hofn','Vardo','Helvig','Bjurholm','Blonduos',
                'Helluland','Hayarano','Akkeshi','Reading','Nelson','Arcadia',
                'Kiyobico','Takazaki','Biruwa','Shinobi','Pauma','Valais','Kinsale',
                'Mahuti','Eden','Vaiku','Colmar','Gordes','Maeva','Riroua','Nidoma','Talu']

data = []
data.append(('obs','Name','Age','island','house number'))
total = 1
for i in city_list:
        num_of_house = []
        driver.get("https://islands.smp.uq.edu.au/village.php?"+ i)
        soup1 = BeautifulSoup(driver.page_source, 'html5lib')
        num = soup1.find_all('div',attrs={'class':'houseid'})
        num_of_house.append(num[-1].text)
        print(i+':'+num[-1].text)
        range_total_house = int(num[-1].text)+ 1
        #print(total_house)
        for n in range(0,range_total_house):
                element = driver.find_element_by_xpath("//img[@onclick='getHouse("+str(n)+");\']")
                webdriver.ActionChains(driver).move_to_element(element ).click(element ).perform()
                sleep(1)
                soup3 = BeautifulSoup(driver.page_source, 'html5lib')
                print(soup3.find('div',attrs={'id':'title'}).text)
 
                soup2 = BeautifulSoup(driver.page_source, 'html5lib')
                num_p = soup2.find_all('td',attrs={'class':'resident'})
                print('number of people: '+ str(len(num_p)))
                # range_total_people = int(num_p[-1].text)+ 1
                # print("total people: " + str(range_total_people))

                if 'This house is empty' not in soup3.get_text():
                        
                        print("This house is not empty")
                        #driver.find_element_by_xpath("//table[@class='residents']/tbody[1]/tr[1]/td[1]/a[1]").click()

                        element2 = driver.find_element_by_xpath("//table[@class='residents']/tbody[1]/tr[1]/td[1]/a[1]")
                        webdriver.ActionChains(driver).move_to_element(element2 ).click(element2 ).perform()




                        soup4 = BeautifulSoup(driver.page_source, 'html5lib')
                        real_name = soup4.find('div',attrs={'id':'title'}).text #get name
                        age_string = str(soup4.find_all('div',attrs={'class':'storyevent'})[1].text)
                        real_age = str([int(s) for s in age_string.split() if s.isdigit()][0]) #get age
                        #throw participate into group
                        print("name: "+ str(real_name))
                        print("age: "+ str(real_age))
                        print("island: "+ str(i))
                        print('current house: '+str(n+1))
                        data.append((total,real_name,real_age,i,n+1))
                        wb1 = Workbook()
                        ws1 = wb1.active
                        for row in data:
                                ws1.append(row)
                        wb1.save('people.xlsx')
                        driver.get("https://islands.smp.uq.edu.au/village.php?"+ i)
                        total = total + 1
                else:
                        print("house is empty")
                        continue
                
