from io import BytesIO
import requests
import requests.cookies
from http import cookiejar
from PIL import Image
import re
import logging
import random
from datetime import datetime, date
import time
import configData

PHPSESSID = None
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'netsaleop.1905.com',
    'Referer': configData.url['base'] + '/index.php'
}
loginData = {'username': '', 'password': '', 'verify': ''}


def inputuser():
    print('验证码')
    print('输入登录名:')
    loginData['username'] = str(input())
    print('输入密码:')
    loginData['password'] = str(input())

    return


def login():
    loginurl = configData.url["base"] + configData.url["login"]
    inputuser()
    print(loginData)
    r = requests.post(loginurl, loginData)
    print(r.text)
    PHPSESSID = r.headers['Set-Cookie']
    print(PHPSESSID)
    return PHPSESSID


def loadOrder():
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'Content-Type': 'application/download',
        'Cookie': l,
        'Origin': 'netsaleop.1905.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) ApiPost/2.4.106 Chrome/69.0.3497.106 Electron/4.0.0 Safari/537.36'
    }
    print(headers)
    cinema_id=None
    url_u = 'http://netsaleop.1905.com/index.php?s=/admin/report/exportOrderList/cinema_id/%s/app_id/0,%s/' \
            'order_start_time/%s/order_end_time/%s/session_start_time/%s/session_end_time/%s'%()
    rs = requests.get(url_u, headers=headers, verify=False)
    time1 = str(int(time.time()))
    print(time1)
    filename = "excel/%s.xls" % time1
    print(filename)
    fp = open(filename, "wb")
    fp.write(rs.content) 
    fp.close()


if __name__ == '__main__':
    s = requests.session()
    l = login()
    print('开始获取订单详情', '登录状态：' + l)
    logging.info('info 信息')
    time.sleep(2)
    loadOrder()
