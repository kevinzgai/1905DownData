from io import BytesIO
import requests
import requests.cookies
import logging
import time
import datetime
import configData
import io

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
    #print(r.text)
    PHPSESSID = r.headers['Set-Cookie']
    print('登录成功','登录识别码为：%s'%PHPSESSID)
    return PHPSESSID


def get_apps():
    strlist = ''
    for app in configData.applist:
        strlist += app['id'] + ','
    return strlist[:-1]


def loadOrder(cinema, order_start_time, order_end_time, session_end_time):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'Content-Type': 'application/download',
        'Cookie': l,
        'Origin': 'netsaleop.1905.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) ApiPost/2.4.106 Chrome/69.0.3497.106 Electron/4.0.0 Safari/537.36'
    }
    # print(headers)
    url_u = 'http://netsaleop.1905.com/index.php?s=/admin/report/exportOrderList/cinema_id/%s/app_id/0,%s/' \
            'order_start_time/%s/order_end_time/%s/session_start_time/%s/session_end_time/%s' \
            % (cinema['id'], get_apps(), order_start_time, order_end_time, session_start_time, session_end_time)
    rs = requests.get(url_u, headers=headers, verify=False)
    filename = cinema['name'] + order_start_time + '至' + order_end_time
    print('已下载excel/%s.xlsx'% filename)
    fp = open("excel/%s.xlsx" % filename, "wb")
    fp.write(rs.content)
    fp.close()


if __name__ == '__main__':
    print('该程序拉取放映时间为 当前时间+%s天，如有不合理请联系开发者修改' % configData.add_days)
    pass
    l = login()
    print('开始获取订单详情', '登录状态：' + l)
    logging.info('info 信息')
    time.sleep(2)
    print('请输入销售时间 格式：2019-01-01')
    order_start_time = input()
    print('请输入销售结束时间 格式：2019-01-08')
    order_end_time = input()
    session_start_time = order_start_time
    end_day = datetime.datetime.now() + datetime.timedelta(days=configData.add_days)
    session_end_time = end_day.strftime('%Y-%m-%d')
    for cinema in configData.cinemalist:
        print('开始获取影城' + cinema['name'] + '数据')
        time.sleep(1)
        print('当前获取播放截止时间 ' + session_end_time + ' 正在拉取数据请稍后。。。。。')
        loadOrder(cinema, order_start_time, order_end_time, session_end_time)
    print('下载完成！！！')
