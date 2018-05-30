'''
此脚本是通过模拟登陆公司管理系统，来查看打卡时间，可以节省使用浏览器登陆操作的时间
'''
import requests
from bs4 import BeautifulSoup
import base64
import datetime
import time
import http.cookiejar
#如果lxml包没有etree，则需要注意版本，安装相应的.whl
from lxml import etree

ss = requests.session()
#登陆请求页面地址
loginUrl = "http://192.168.15.26/C6/Jhsoft.Web.login/AjaxForLogin.aspx"
#打卡请求页面地址
punchTimeUrl = "http://192.168.15.26/C6/JHSoft.web.HRMAttendance/Attendance_Message.aspx?"
#用户名和用户密码需要自己补充
userName = ""
userPwd = ""
#用户名及密码参数用base64进行编码，再对编码按utf-8进行解码
userName = base64.b64encode(userName.encode('utf-8'))
userPwd = base64.b64encode(userPwd.encode('utf-8'))
userName = userName.decode('utf-8')
userPwd = userPwd.decode('utf-8')
typeLogin = "login"
#表单数据
formData = {'type':typeLogin,'loginCode': userName,'pwd':userPwd}

date = datetime.datetime.now().strftime('%Y-%m-%d')
#获取cookie对象
ss.cookies = http.cookiejar.MozillaCookieJar(filename="gwtt_cookie");
try:
    #加载cookie内容
    ss.cookies.load(ignore_discard=True)
except:
    #若加载异常（可能还不存在cookie）则重新登录，并保存cookie
    response = ss.post(loginUrl,data=formData)
    ss.cookies.save(ignore_discard=True)
params = {'style' : 'style','date':date,'u':'0540'}
#发起请求，获取打卡时间页面
response = ss.get(punchTimeUrl,params=params,allow_redirects=False)
#返回结果失败（一般是由于cookie失效），重新登录，并保存cookie
if response.status_code != 200:
    ss.cookies.clear()
    response = ss.post(loginUrl,data=formData)
    ss.cookies.save(ignore_discard=True)
    response = ss.get(punchTimeUrl,params=params)
#对打开时间页面进行解析
soup = BeautifulSoup(str(response.text),'html.parser')
selector = etree.HTML(response.text)
content = selector.xpath("//div[@id='divTable']/table/tr[2]/td/text()")
name = selector.xpath("//*[@id='form1']/div/table/tr/td[2]/input/@value")
print(content)
punchTime = soup.findAll('td')[-1]

punchTime = str(punchTime)[6:-5]
print(punchTime)
startTime = punchTime.split()[0]

print(name)
print(startTime)
