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
#创建一个日志
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#创建一个文件handler
handler=logging.FileHandler('weio.log')
handler.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)

#创建一个formatter
formatter=logging.Formatter('%(asctime)s -%(name)s - %(levelname)s - %(message)s' )
handler.setFormatter(formatter)
logger.addHandler(handler)

#控制台输出
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
    
#打开Firefox浏览器 设定等待加载时间 访问URL 加载已有的配置
profile_dir="/home/bewolf/.mozilla/firefox/o9m2lfa2.default" 
fp=webdriver.FirefoxProfile(profile_dir)  
driver = webdriver.Firefox(fp)
    #driver_detail=webdriver.Firefox()

wait = ui.WebDriverWait(driver,10)    
#driver.get("http://s.weibo.com/weibo/%2523%25E5%25A4%25AA%25E9%2598%25B3%25E7%259A%2584%25E5%2590%258E%25E8%25A3%2594%2523&typeall=1&suball=1&timescope=custom:2016-03-01:2016-03-02&Refer=g")    
message_dic={}

#获取页数
def getPages():
    wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='W_pages']/span/div/ul/li"))
    pagelists=driver.find_elements_by_xpath("//div[@class='W_pages']/span/div/ul/li")
    print len(pagelists)
    return len(pagelists)
#driver.find_elements_by_xpath
def getdetail_message(message_x):
	for message in message_x:
		i=message.text
		#print i
		return i    
def getdetail_link(message_x):
	for message in message_x: 
		i=message.get_attribute("href")
		return i
		#print i   
#读取某个文件获取url_list
def read_url(file_url):
    url_list=[]
    for line in open(file_url):
                    lineline = line.rstrip('\n') 
                    url_list.append(lineline)
    return url_list
#去掉url的最后一个字符
def DelLastChar(str):
    str_list=list(str)
    for i in range(1,8):
        str_list.pop()
    return "".join(str_list)

#获取信息    
def getdetail(filename): 
    message_total=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']")
    page_message_number=len(message_total)
    logger.info( "共有"+str(page_message_number)+"条博文")
    #print "此url下共有"+str(page_message_number)+"条博文"
    file=codecs.open(filename,"a",encoding='utf-8')
    #file.write("这是第"+str(pagenumber)+"页"+"\n")
    for i in range(1,page_message_number+1):
        #获取博文的博主以及主页链接
        message_name_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//div[@class='feed_content wbcon']/a") 
        message_dic["message_name"]=getdetail_message(message_name_element)
        message_dic['message_owner_link']=getdetail_link(message_name_element)
        #获取博文时间及博文主页
        message_time_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//div[@class='feed_from W_textb']/a[1]") 
        message_dic["message_time"]=getdetail_message(message_time_element)
        message_dic["message_link"]=getdetail_link(message_time_element)
        #获取博文的设备
        message_equipment_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//div[@class='feed_from W_textb']/a[2]")
        message_dic["message_equipment"]=getdetail_message(message_equipment_element) 
        #获取博文的收藏数
        message_collection_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//div[@class='feed_action clearfix']/ul/li[1]")
        message_dic["message_collection_number"]=getdetail_message(message_collection_element)
        #获取博文的评论数
        message_comment_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//div[@class='feed_action clearfix']/ul/li[2]")
        message_dic["message_comment_number"]=getdetail_message(message_comment_element)
        #获取博文的转发数 
        message_forward_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//div[@class='feed_action clearfix']/ul/li[3]")
        message_dic["message_forward_number"]=getdetail_message(message_forward_element)
        #获取博文的点赞数 
        message_like_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//div[@class='feed_action clearfix']/ul/li[4]")
        message_dic["message_like_number"]=getdetail_message(message_like_element)
        #获取内容
        content_element=driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']"+"["+str(i)+"]"+"//p[@class='comment_txt']")
        message_dic["message_content"]=getdetail_message(content_element)
        #return message_dic
        #print "正在获取"+str(pagenumber)+"页的博文"
        line = json.dumps(message_dic,ensure_ascii=False,sort_keys=False) + "\n"
        file.write(line)

    logger.info("已获取"+str(page_message_number)+"条博文")
    file.close()
    sleeptime=random.randint(15,40)
    logger.info("休息"+str(sleeptime)+"秒")
    #print "休息"+str(sleeptime)+"秒"
    time.sleep(sleeptime)

       
    
    



def main():
    
    #SUMRESOURCES = 0 #全局变量 记录资源总数(尽量避免)    
    #获取该文本下的网址
    #file_url保存按时间分配的url的文本，url_list保存读取的url的列表，url_time表示列表中的某一个url，pageurl是没一页的url
    file_url="/home/bewolf/document/number1.txt"
    url_time_list=read_url(file_url)
    url_list_len=len(url_time_list)
    for i in range(0,url_list_len):
        url_time=str(url_time_list[i])
        driver.get(url_time)
        #减少超时造成的影响
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='feed_content wbcon']/a")) 
        logger.info("已加载网页"+str(url_time)) 
        page_number= getPages()
        logger.info("该网页有"+str(page_number)+"页面")
        url_page_first=DelLastChar(url_time)+"page="
        topictime=url_time[-29:-8]
        filename=topictime+".json"
        for j in range(1,page_number+1):
                logger.info( "加载第"+str(j)+"页")
                #print "加载第"+str(j)+"页"
                pageurl=url_page_first+str(j)
                driver.get(pageurl)
                logger.info("加载完毕，开始获取")
                #print "加载完毕，开始获取" 
                getdetail(filename)
        urlsleeptime=random.randint(60,150)
        logger.info("url结束，休息"+str(urlsleeptime))
        time.sleep(urlsleeptime)

       
        

main() 
