# -*- coding: utf-8 -*-
# !/usr/bin/env python
class TTSOffline(object):
    """Offline tts using """
    def __init__(self):
        pass
    def text2audio(self,text,path=''):
        """
        文本转语音，mp3格式，获得的mp3格式语音以当前时间命名。
        :param text: 必填，合成的文本，使用UTF-8编码，请注意文本长度必须小于1024字节
        :param path: 语音存储路径
        :return:
        """
