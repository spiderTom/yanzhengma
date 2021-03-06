yuncode/                                                                                            0000755 0000772 0000772 00000000000 13202242575 011136  5                                                                                                    ustar   jack                            jack                                                                                                                                                                                                                   yuncode/match.py                                                                                    0000644 0000772 0000772 00000000265 13065623274 012615  0                                                                                                    ustar   jack                            jack                                                                                                                                                                                                                   # conding = utf-8
import yunCode

filepath = u'image/'
filename = u'14713478019.png'

def findCode(filename)
    code = yunCode.yunDamaFunction(filename)
    return code

                                                                                                                                                                                                                                                                                                                                           yuncode/YDMHTTPDemo.py                                                                              0000644 0000772 0000772 00000013634 13065623274 013463  0                                                                                                    ustar   jack                            jack                                                                                                                                                                                                                   import httplib, mimetypes, urlparse, json, time

######################################################################

# 错误代码请查询 http://www.yundama.com/apidoc/YDM_ErrorCode.html
# 所有函数请查询 http://www.yundama.com/apidoc

# 1. http://www.yundama.com/index/reg/developer 注册开发者账号
# 2. http://www.yundama.com/developer/myapp 添加新软件
# 3. 使用添加的软件ID和密钥进行开发，享受丰厚分成

# 用户名
username    = 'username'

# 密码
password    = 'password'                            

# 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
appid       = 1                                     

# 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
appkey      = '22cc5376925e9387a23cf797cb9ba745'    

# 图片文件
filename    = 'getimage.jpg'                        

# 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
codetype    = 1004

# 超时时间，秒
timeout     = 60                                    

# 检查
if (username == 'username'):
    print '请设置好相关参数再测试'
else:
    # 初始化
    yundama = YDMHttp(username, password, appid, appkey)

    # 登陆云打码
    uid = yundama.login();
    print 'uid: %s' % uid

    # 查询余额
    balance = yundama.balance();
    print 'balance: %s' % balance

    # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
    cid, result = yundama.decode(filename, codetype, timeout);
    print 'cid: %s, result: %s' % (cid, result)

######################################################################

class YDMHttp:

    apiurl = 'http://api.yundama.com/api.php'
    
    username = ''
    password = ''
    appid = ''
    appkey = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username  
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        try:
            response = post_url(self.apiurl, fields, files)
            response = json.loads(response)
        except Exception as e:
            response = None
        return response
    
    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001
    
    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

######################################################################

def post_url(url, fields, files=[]):
    urlparts = urlparse.urlsplit(url)
    return post_multipart(urlparts[1], urlparts[2], fields, files)

def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('Host', host)
    h.putheader('Content-Type', content_type)
    h.putheader('Content-Length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files=[]):
    BOUNDARY = 'WebKitFormBoundaryJKrptX8yPbuAJLBQ'
    CRLF = '\r\n' 
    L = [] 
    for field in fields:
        key = field
        value = fields[key]
        L.append('--' + BOUNDARY) 
        L.append('Content-Disposition: form-data; name="%s"' % key) 
        L.append('') 
        L.append(value) 
    for field in files:
        key = field
        filepath = files[key]
        L.append('--' + BOUNDARY) 
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filepath))
        L.append('Content-Type: %s' % get_content_type(filepath)) 
        L.append('')
        L.append(open(filepath, 'rb').read())
    L.append('--' + BOUNDARY + '--') 
    L.append('') 
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY 
    return content_type, body 

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

######################################################################
                                                                                                    yuncode/yunCode.py                                                                                  0000644 0000772 0000772 00000015472 13065623274 013135  0                                                                                                    ustar   jack                            jack                                                                                                                                                                                                                   # -*- coding: utf-8 -*-
import httplib, mimetypes, urlparse, json, time
######################################################################
class YDMHttp:
    apiurl = 'http://api.yundama.com/api.php'
    username = ''
    password = ''
    appid = ''
    appkey = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        try:
            response = post_url(self.apiurl, fields, files)
            response = json.loads(response)
        except Exception as e:
            response = None
        return response

    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

######################################################################

def post_url(url, fields, files=[]):
    urlparts = urlparse.urlsplit(url)
    return post_multipart(urlparts[1], urlparts[2], fields, files)

def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('Host', host)
    h.putheader('Content-Type', content_type)
    h.putheader('Content-Length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files=[]):
    BOUNDARY = 'WebKitFormBoundaryJKrptX8yPbuAJLBQ'
    CRLF = '\r\n'
    L = []
    for field in fields:
        key = field
        value = fields[key]
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for field in files:
        key = field
        filepath = files[key]
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filepath))
        L.append('Content-Type: %s' % get_content_type(filepath))
        L.append('')
        L.append(open(filepath, 'rb').read())
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def demo():
    # 鐢ㄦ埛鍚�
    username    = 'asafish83'

    # 瀵嗙爜
    password    = 'Tryqtyl2'

    # 杞欢锛╋激锛屽紑鍙戣�呭垎鎴愬繀瑕佸弬鏁般�傜櫥褰曞紑鍙戣�呭悗鍙般�愭垜鐨勮蒋浠躲�戣幏寰楋紒
    appid       = 1

    # 杞欢瀵嗛挜锛屽紑鍙戣�呭垎鎴愬繀瑕佸弬鏁般�傜櫥褰曞紑鍙戣�呭悗鍙般�愭垜鐨勮蒋浠躲�戣幏寰楋紒
    appkey      = '22cc5376925e9387a23cf797cb9ba745'

    # 鍥剧墖鏂囦欢
    filename    = '147142357872'

    # 楠岃瘉鐮佺被鍨嬶紝# 渚嬶細1004琛ㄧず4浣嶅瓧姣嶆暟瀛楋紝涓嶅悓绫诲瀷鏀惰垂涓嶅悓銆傝鍑嗙‘濉啓锛屽惁鍒欏奖鍝嶈瘑鍒巼銆傚湪姝ゆ煡璇㈡墍鏈夌被鍨� http://www.yundama.com/price.html
    codetype    = 1004

    # 瓒呮椂鏃堕棿锛岀
    timeout     = 60

    # 妫�鏌�
    if (username == 'username'):
        print '璇疯缃ソ鐩稿叧鍙傛暟鍐嶆祴璇�'
    else:
        
        # 鍒濆鍖�
        yundama = YDMHttp(username, password, appid, appkey)

        # 鐧婚檰浜戞墦鐮�
        uid = yundama.login();
        print 'uid: %s' % uid

        # 鏌ヨ浣欓
        balance = yundama.balance();
        print 'balance: %s' % balance

        # 寮�濮嬭瘑鍒紝鍥剧墖璺緞锛岄獙璇佺爜绫诲瀷ID锛岃秴鏃舵椂闂达紙绉掞級锛岃瘑鍒粨鏋�
        cid, result = yundama.decode(filename, codetype, timeout);
        print 'cid: %s, result: %s' % (cid, result)

def yunDamaFunction(filename):
  
    username    = 'asafish83'
    password    = 'Tryqtyl2'
    appid       = 1
    appkey      = '22cc5376925e9387a23cf797cb9ba745'
    #filename    = '1471423247.07'
    # 楠岃瘉鐮佺被鍨嬶紝# 渚嬶細1004琛ㄧず4浣嶅瓧姣嶆暟瀛楋紝涓嶅悓绫诲瀷鏀惰垂涓嶅悓銆傝鍑嗙‘濉啓锛屽惁鍒欏奖鍝嶈瘑鍒巼銆傚湪姝ゆ煡璇㈡墍鏈夌被鍨� http://www.yundama.com/price.html
    codetype    = 1004
    # 瓒呮椂鏃堕棿锛岀
    timeout     = 60
    # 妫�鏌�
    if (username == 'username'):
        print '璇疯缃ソ鐩稿叧鍙傛暟鍐嶆祴璇�'
        return u'', u''
    else:
        # 鍒濆鍖�
        yundama = YDMHttp(username, password, appid, appkey)

        # 鐧婚檰浜戞墦鐮�
        uid = yundama.login();
        print 'uid: %s' % uid

        # 鏌ヨ浣欓
        balance = yundama.balance();
        print 'balance: %s' % balance

        # 寮�濮嬭瘑鍒紝鍥剧墖璺緞锛岄獙璇佺爜绫诲瀷ID锛岃秴鏃舵椂闂达紙绉掞級锛岃瘑鍒粨鏋�
        cid, result = yundama.decode(str(filename), codetype, timeout);
        print 'cid: %s, result: %s' % (cid, result)
        return result

if __name__ == u'__main__':
    demo()
    
                                                                                                                                                                                                      yuncode/bcode.py                                                                                    0000644 0000772 0000772 00000005550 13065623274 012577  0                                                                                                    ustar   jack                            jack                                                                                                                                                                                                                   # -*- coding: cp936 -*-

import requests
import re
import time
import yunCode

#FIX ME. disable requests warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
            u'User-Agent':u'Mozilla/5.0 (Windows NT 6.1; WOW64) App\
            leWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
            }

model = re.compile(u'<title>请输入验证码\s*</title>')

def saveImage(filename, content):
    filename = unicode(time.time()).replace(u'.', u'')
    #filename = filename + u'.png'
    with open(filename, u'wb') as f:
        f.write(content)
    return filename


class CodeAna(object):
    
    def makeSession(self):
        s = requests.session()
        self.session = s

    def makecodeUrl(self, t):
        url = u'http://mp.weixin.qq.com/mp/verifycode?cert=%s' % t
        return url

    def makecodePostParas(self, t, code):
        url = u'http://mp.weixin.qq.com/mp/verifycode'
        paras = {u'cert': unicode(t),
                 u'input': code}
        return url, paras
        

    def postdata(self, url, paras, headers = None):
        if headers is None:
            r = self.session.post(url, data=paras)
        else:
            r = self.session.post(url, data=paras, headers=headers)
        return r

    def getdata(self, url, headers = None):
        if headers is None:
            r = self.session.get(url)
        else:
            r = self.session.get(url, headers=headers)
        return r
    
        r = self.session.get(url)
        return r

    def analysisCode(self, url):
        self.makeSession()
        
        #url = u'http://mp.weixin.qq.com/profile?src=3&timestamp=1471414472&ver=1&signature=2SIYL6prekN-oPlIyvzOmycgrnCFc7hUBl2NGjGrxd9VSJOI7SWhS3vikHwiyw*VhGPPsV8p*ujID16nSfFg0Q=='
        r = self.getdata(url)
        content =  r.text
        #print content
        is_code = model.findall(content)
        if is_code:
            t = time.time()
            headers[u'Referer'] = url
            codeurl = self.makecodeUrl(t)
            r = self.getdata(codeurl)
            imageName = saveImage(unicode(t), r.content)
            print imageName
            time.sleep(3)
            code_input = yunCode.yunDamaFunction(imageName)
            print u'code_input:', code_input
            #code_input = raw_input(u'code:')

            posturl,paras = self.makecodePostParas(t, code_input)
            r = self.postdata(posturl, paras)
            #print r.content
            return r.content
        else:
            #print u'yes'
            #print content
            return "no need dama"
            
            
            
            
            
 
if __name__ == u'__main__':
    code = CodeAna()
    code.analysisCode()
                                                                                                                                                        yuncode/getImage.py                                                                                 0000644 0000772 0000772 00000001524 13065623274 013242  0                                                                                                    ustar   jack                            jack                                                                                                                                                                                                                   # coding = utf-8
import requests
import time

#FIX ME. disable requests warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

filepath = u'image/'

def saveImage(content):
    fname = unicode(time.time()).replace(u'.',u'')
    
    with open(filepath + fname + u'.png', u'wb') as f:
        f.write(content)

def downloadImage(url):
    r = requests.get(url)
    content = r.content
    saveImage(content)

def main():
    url_base = u'http://mp.weixin.qq.com/mp/verifycode?cert='

    for i in xrange(1,1000):
        print i
        random_num = unicode(time.time()).replace(u'.',u'')
        url = url_base + random_num + u'.1738'
        downloadImage(url)

if __name__ == u'__main__':
    main()
    #downloadImage(url)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            