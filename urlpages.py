# coding:utf-8    
    
from selenium import webdriver    
from selenium.webdriver.common.keys import Keys    
import selenium.webdriver.support.ui as ui    
from selenium.webdriver.common.action_chains import ActionChains    
import time        
import re        
import sys 
import json
import codecs
import random
import logging
reload(sys) 
sys.setdefaultencoding('utf8')

profile_dir="/home/bewolf/.mozilla/firefox/o9m2lfa2.default" 
fp=webdriver.FirefoxProfile(profile_dir)  
driver = webdriver.Firefox(fp)
    #driver_detail=webdriver.Firefox()

wait = ui.WebDriverWait(driver,10)    

def getPages():
    wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='W_pages']/span/div/ul/li"))
    pagelists=driver.find_elements_by_xpath("//div[@class='W_pages']/span/div/ul/li")
    print len(pagelists)
    return len(pagelists)

def read_url(file_url):
    url_list=[]
    for line in open(file_url):
                    lineline = line.rstrip('\n') 
                    url_list.append(lineline)
    return url_list

def  main():
	file_url="/home/bewolf/document/pagetestnumber.txt"
	url_list=read_url(file_url)
	print url_list
	file=codecs.open("url_page_number.json","a",encoding='utf-8')
	url_page_numbers={}
	for i in range(0,len(url_list)):
		url_page_numbers["url"]=url_list[i]
		url=str(url_list[i])
		print url
		driver.get(url)
		number=getPages()
		url_page_numbers["pagenumber"]=number
		line = json.dumps(url_page_numbers,ensure_ascii=False,sort_keys=False) + "\n"
		file.write(line)
		randomtime=random.randint(3,15)
		time.sleep(randomtime)
main()