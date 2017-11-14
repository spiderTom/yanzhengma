import urllib
import urllib2
import cookielib
import re
import socket
from bs4 import BeautifulSoup


def Navigate(url, data={}):  # 定义连接函数，有超时重连功能
    tryTimes = 0
    while True:
        if (tryTimes > 20):
            print("多次尝试仍无法链接网络，程序终止")
            break
        try:
            if (data == {}):
                req = urllib2.Request(url)
            else:
                req = urllib2.Request(url, urllib.urlencode(data))
            req = urllib2.urlopen(req).read()
            tryTimes = tryTimes + 1
        except socket.error:
            print("连接失败，尝试重新连接")
        else:
            break
    return req


try:
    cookie = cookielib.CookieJar()
    cookieProc = urllib2.HTTPCookieProcessor(cookie)
except:
    raise
else:
    opener = urllib2.build_opener(cookieProc)
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
    urllib2.install_opener(opener)

url = "https://passport.jd.com/uc/login"
login = func.Navigate(url)
loginSoup = BeautifulSoup(login)
# 查找登陆参数中的uuid
uuid = loginSoup.find_all("form")[0].find_all("input")[0]['value']
# print uuid

# 查找登陆参数中的随机值，class为clr
clr = loginSoup.find_all("span", "clr")[0]
clrName = clr.find_next_siblings("input")[0]['name']
clrValue = clr.find_next_siblings("input")[0]['value']
# print clrName,clrValue

url = "http://passport.jd.com/uc/loginService"
# print url

postData = {
    'loginname': self.user,
    'nloginpwd': self.password,
    'loginpwd': self.password,
    # 'machineNet':'',
    # 'machineCpu':'',
    # 'machineDisk':'', str(clrName):str(clrValue),
    'uuid': uuid,
    'authcode': ''
}
passport = Navigate(url, postData)
print(passportSoup)