""" 模拟登陆路由器，发送拨号信号，控制路由器重新联网以改变ip地址。
路由器型号：斐讯K2p
固件：官方修改版
路由器IP地址：192.168.2.1
"""

import requests
import json


def redial():
    """
    returns:: 0 or -10210
    0为正常，其他为错误
    """
    url = "http://192.168.2.1/cgi-bin/"
    payload = "{\"method\":\"set\",\"module\":{\"security\":{\"login\":{\"username\":\"admin\",\"password\":\"OTgwMjA4\"}}},\"_deviceType\":\"pc\"}"
    headers = {
        'Host': "192.168.2.1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0",
        'Accept': "*/*",
        'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        'Accept-Encoding': "gzip, deflate",
        'Referer': "http://192.168.2.1/cgi-bin",
        'Content-Type': "application/json",
        'X-Requested-With': "XMLHttpRequest",
        'Connection': "keep-alive",
        'cache-control': "no-cache",
        }
    headers_send_signal = {
        'Host': "192.168.2.1",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0",
        'Accept': "*/*",
        'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        'Accept-Encoding': "gzip, deflate",
        'Referer': "http://192.168.2.1/cgi-bin",
        'Content-Type': "application/json",
        'X-Requested-With': "XMLHttpRequest",
        'Content-Length': "297",
        'Connection': "keep-alive",
        'cache-control': "no-cache",
        }

    payload_send_signal='{"method":"set","module":{"network":{"wan":{"protocol":"pppoe","clone_mode":"0","mac":"","source_mac":"74%3A7D%3A24%3A53%3A17%3A1C"},"pppoe":{"username":"15179921554%40lan","password":"348262","dial_mode":"0","server":"","mtu":"1480","dns_mode":"0","dns_pri":"","dns_sec":""}}},"_deviceType":"pc"}'

    s = requests.Session()
    response = s.post( url, data=payload, headers=headers)
    json_response=json.loads(response.text)
    if json_response['error_code']==0:
        stok=json_response['module']['security']['login']['stok']
    else :
        return -1
    url_send_signal='http://192.168.2.1/cgi-bin/stok=%s/data/network'


    response_send_signal=s.post(url_send_signal%stok,data=payload_send_signal,headers=headers_send_signal)
    error_code=json.loads(response_send_signal.text)['error_code']
    return error_code  