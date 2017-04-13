# -*- coding: utf-8 -*-
# !/usr/bin/env python
import wave
import urllib, urllib2, pycurl
import base64
import json
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')


class  TTSBaidu(object):
    """TTS usiong Baidu Vocie API"""
    def __init__(self):
        pass
            
    ##get tokenormat
    def get_token(self):
        apiKey = "0XyzNfIwZeSqDN8oZWR54Qon"
        secretKey = "92971d401d3df1bd2869afebc04df63b"
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials" + "&client_id=" + apiKey + "&client_secret=" + secretKey
        res = urllib2.urlopen(auth_url)
        json_data = res.read()
        return json.loads(json_data)['access_token']


    ##post text to server 使用云端进行语音合成
    def use_cloud(self,token, text, spd, pit, vol, per):
        cuid = "38:c9:86:13:93:1f"  # my Mac MAC
        srv_url = 'http://tsn.baidu.com/text2audio'
        values = {'cuid': cuid, 'tok': token, 'tex': text.encode("UTF-8"), 'lan': "zh", 'ctp': 1, 'spd': spd, 'pit': pit,
                  'vol': vol, 'per': per}
        post_data = urllib.urlencode(values)
        req = urllib2.Request(srv_url, post_data)
        response = urllib2.urlopen(req)
        return response


    def store_mp3(self,mp3_data, path):
        # current_time = time.strftime('%Y%m%d-%H:%M:%S', time.localtime(time.time()))
        f = open(path + '.mp3', 'wb')
        f.writelines(mp3_data)
        f.close()
        return f.name


    def text2audio(self,text, path='', spd=5, pit=5, vol=5, per=0):
        """
        文本转语音，mp3格式，获得的mp3格式语音以当前时间命名。
        :param text: 必填，合成的文本，使用UTF-8编码，请注意文本长度必须小于1024字节
        :param path: 语音存储路径
        :param spd:选填，语速，取值0-9，默认为5中语速
        :param pit:选填，音调，取值0-9，默认为5中语调
        :param vol:选填，音量，取值0-9，默认为5中音量
        :param per:选填，发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
        :return:文件名
        """
        if len(text) >= 1024:
            raise KeyError("text length should be less than 1024 bytes")
        token = self.get_token()
        response = self.use_cloud(token, text, spd, pit, vol, per)
        content_type = response.info().getheader('Content-Type')
        if content_type.startswith('application/json'):
            response_text = response.read().decode("utf-8")
            json_result = json.loads(response_text)
            raise LookupError("%d - %s" %
                              (json_result['err_no'], json_result['err_msg']))
        elif content_type.startswith('audio/mp3'):
            # return response.read()
            file_name = self.store_mp3(response.read(), path)
            return file_name

if __name__ == '__main__':
    mytts = TTSBaidu()
    text = '车势科技Autoforce成立于2016年初，是一家专为汽车行业提供“沉浸式、一体化”数字销售解决方案的科技公司。车势科技基于VR+SaaS技术，实现1:1实景实车还原、销售顾问全时在线，让消费者能够随时随地通过线上虚拟经销店看车试车订车，一站式促成购车意向。'
    # text = '车势科技..'
    print type(mytts.text2audio(text, pit=5, per=3))
