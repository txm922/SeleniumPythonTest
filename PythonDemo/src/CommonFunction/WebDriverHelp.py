#coding=utf-8
'''
Created on 2015年8月12日

WebDriverHelp用来存放所有页面操作用到公用方法

@author: QLLU
'''
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
global G_WEBDRIVER, G_BROWSERTYTPE,driver
 
class WebDriverHelp(object):
    '''
        本类主要完成页面的基本操作，如打开指定的URL，对页面上在元素进行操作等
    '''
 
    def  __init__(self,btype="close",atype="firefox",ctype="local"):
        '''
                根据用户定制，打开对应的浏览器
        @param bType: 开关参数，如果为close则关闭浏览器
        @param aType:打开浏览器的类型，如chrome,firefox,ie等要测试的浏览器类型
        @param cType:打开本地或是远程浏览器： local,本地；notlocal：远程        '''
        global driver
        if(  btype == "open" ):           
            if(  atype == "chrome" ):
                if(ctype == "local"):   
                    driver = webdriver.Chrome()
#                     driver.maximize_window()
                elif(ctype == "notlocal"): 
                    print "不能打开chrome"

            elif(  atype == "ie" ):
                if(ctype == "local"): 
                    driver = webdriver.Ie()
#                     driver.maximize_window()
                elif(ctype == "notlocal"):
                    print "不能打开IE"  
              
            elif(  atype == "firefox" ):
                if(ctype == "local"):
                    driver = webdriver.Firefox()
#                     driver.maximize_window()
                elif(ctype == "notlocal"): 
                    print "不能打开firefox" 

                                  
        self.driver = driver
 
    def  setup(self,logintype):
        '''
                定制测试URL，可分为单机版、云版
        @param loginplace: 指定测试的URL： onpre:单机版测试地址，cloud:云版测试地址
        ysh:原始会测试地址 zhengshiysh:正式原始会测试地址
        '''
        try:
            grn403_url = "http://10.60.3.126/cgi-bin/cbgrn/grn.cgi"    
            grndev_url = "http://qllu.cybozu-dev.cn" 
            grncn_url = "https://qatest01.cybozu.cn"           
 
            if(logintype=="grn403"):
                self.driver.get(grn403_url)
            elif(logintype=="grndev"):
                self.driver.get(grndev_url)
            elif(logintype=="grncn"): 
                self.driver.get(grncn_url)                   
            else:
                print '路径错误！'
            self.driver.implicitly_wait(1)
        except NoSuchElementException:
            print 'URL Error！！'    
              
    def  teardown(self):
        '''
        close browser
        '''       
        self.driver.quit()
                
    def  geturl(self,url):
        '''
                打开指定的网址
        @param url: 要打开的网址
        '''
        self.driver.get(url)    
        
    
    def clickitem(self,findby,elmethod):
        '''
                通过定制定位方法，在对应的项目上执行单击操作
        @param findby: 定位方法，如：byid,byname,byclassname,byxpath等
        @param elmethod: 要定位元素的属性值 ，如：id,name,class name,xpath，text等
        '''
        if(findby == 'byid'):
            self.driver.find_element_by_id(elmethod).click()
        elif(findby == 'byname'):
            self.driver.find_element_by_name(elmethod).click()
        elif(findby == 'byxpath'):
            self.driver.find_element_by_xpath(elmethod).click()
        elif(findby == 'bytext'):
            self.driver.find_element_by_text(elmethod).click()
        elif(findby == 'byclassname'):
            self.driver.find_element_by_class_name(elmethod).click()
        elif(findby == 'bycss'):
            self.driver.find_element_by_css_selector(elmethod).click()         
            
    def clearvalue(self,findby,elmethod):
        '''
                通过定制定位方法，在输入框中输入值
        @param findby: 定位方法，如：byid,byname,byclassname,byxpath等
        @param elmethod: 要定位元素的属性值 ，如：id,name,class name,xpath等
        @param value: 要给文本框输入的值
        '''
        if(findby == 'byid'):
            self.driver.find_element_by_id(elmethod).clear()
        elif(findby == 'byname'):
            self.driver. find_element_by_name(elmethod).clear()
        elif(findby =='byclassname'):
            self.driver.find_element_by_class_name(elmethod).clear()
        elif(findby == 'byxpath'):
            self.driver.find_element_by_xpath(elmethod).clear()          
      
    def inputvalue(self,findby,elmethod,value):
        '''
                通过定制定位方法，在输入框中输入值
        @param findby: 定位方法，如：byid,byname,byclassname,byxpath等
        @param elmethod: 要定位元素的属性值 ，如：id,name,class name,xpath等
        @param value: 要给文本框输入的值
        '''
        if(findby == 'byid'):
            self.driver.find_element_by_id(elmethod).send_keys(value)
        elif(findby == 'byname'):
            self.driver.find_element_by_name(elmethod).send_keys(value)
        elif(findby =='byclassname'):
            self.driver.find_element_by_class_name(elmethod).send_keys(value)
        elif(findby == 'byxpath'):
            self.driver.find_element_by_xpath(elmethod).send_keys(value)

    def  selectvalue(self,findby,select,selectvalue):
        '''
                通过定制定位方法和要选择项的文本，选择指定的项目
        @param findby:定位方法，如：byid,byname,byclassname等
        @param select: 要执行选择操作的下拉框句柄
        @param selectvalue: 下拉框中要选择项的文本
        '''
        if(findby == 'byid'):
            select = Select(self.find_element_by_id(select))
        elif(findby =='byname'):
            select = Select(self.find_element_by_name(select))
        elif(findby =='byclassname'):
            select = Select(self.find_element_by_classname(select))
        select.select_by_visible_text(selectvalue)           

            
    def gettext(self,findby,elmethod):
        '''
                通过定制定位方法，获取指定元素的文本
        @param findby: 定位方法，如：byid,byname,byxpath等
        @param elmethod: 要定位元素的属性值 ，如：id,name,xpath等
        @return: 返回获取到的元素文本
        '''
        if(findby == 'byid'):
            return self.driver.find_element_by_id(elmethod).text
        elif(findby == 'byname'):
            return self.driver.find_element_by_name(elmethod).text
        elif(findby == 'byxpath'):
            return self.driver.find_element_by_xpath(elmethod).text
        elif (findby=='byclassname'):
            return self.driver.find_element_by_class_name(elmethod).text
        elif (findby=='bycss'):
            return self.driver.find_element_by_css_selector(elmethod).text                 
        
           
            
            