# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:03:27 2018

"""
# Hong Kong post scraper
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(executable_path="chromedriver.exe")
allstreetnames = pd.read_excel('allstreetnames.xlsx')

driver.get('https://www.hongkongpost.hk/correct_addressing/index.jsp?lang=en_US')
def runthrough(term):
      driver.find_element_by_id('r1').click()
      inputElement = driver.find_element_by_id("streetinput")
      inputElement.send_keys(term)
      driver.find_element_by_id('rdsearch2').click()
            
      src = driver.page_source
      parser = BeautifulSoup(src,'lxml')
      pagenumber = len(parser.select('select[id=selectspage] > option'))
      currentpgnumber = int(parser.select('select[id=selectspage] > option[selected]')[0].text)
      listofdfs = []
            
      def getdf():
            src = driver.page_source
            parser = BeautifulSoup(src,'lxml')
            district = parser.findAll('td',{"class":"tdstyle",'width':['220pt']})
            street = parser.findAll('td',{"class":"tdstyle",'width':['250pt']})
            building = parser.findAll('td',{"class":"tdstyle",'width':['280pt']})
            a = zip(district,street,building)
            templist = []
            for k,(d,s,b) in enumerate(a):
                  templist.append([d.text,s.text,b.text])
            df = pd.DataFrame(templist,columns=['District','Street','Building'])
            return(df)
      
      currentpgnumber = 1
      while currentpgnumber < pagenumber:
            listofdfs.append(getdf())
            driver.find_element_by_xpath('//*[@id="saddrpage"]/a[2]/font/b').click()
            print('current page: '+str(currentpgnumber))
            currentpgnumber +=1
            print('current term: '+term)
      else:
            listofdfs.append(getdf())
            df = pd.concat(listofdfs)
            return(df)
            
listofdfs2 = []
for i in allstreetnames['Chinese Street Name']:
      try:
            listofdfs2.append(runthrough(i))
      except:
            alert = driver.switch_to_alert()
            alert.accept()
      time.sleep(4)
      driver.find_element_by_id('rdreset2').click()


wb = pd.ExcelWriter('Alladdresses.xlsx')
alldfs = pd.concat(listofdfs2)
alldfs.to_excel(wb)
wb.save()


driver.close()
