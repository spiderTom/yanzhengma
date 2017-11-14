#coding:utf-8
import unittest
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

print("asdfwerwerwe")


class Miaosha:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url_login = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F"


    def saveHtml(self, fileName):
        f = open(fileName, 'w+')
        #f.write(self.driver.page_source.encode('utf-8'))
        f.close()

    def loginJD(self):
        driver = self.driver
        driver.get(self.url_login)
        #print driver.title
        elem = driver.find_element_by_name("loginname")
        elem.send_keys("tomtubo")
        elem = driver.find_element_by_name("nloginpwd")
        elem.send_keys("AAAsss111")
        elem.send_keys(Keys.RETURN)
        #login finished
        #print driver.title
        #print driver.page_source
        #driver.get(self.url_query)
        #txtStartDate

        ##print driver.page_source
        #self.saveHtml("111.html")
        #self.capturePicture()


    def tearDown(self):
        pass
        #self.driver.close()


print("sdfasdfasd")	
aaa = Miaosha()
aaa.loginJD()
