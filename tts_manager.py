# -*- coding: utf-8 -*-
# !/usr/bin/env python
import tts_baidu
import tts_google
import tts_offline
import re
import threading
import time
import os
import subprocess

class TTSManger(object):
    #TODO：加入缓冲机制
    #TODO:百度语音识别的API可能不稳定或者报错，此时的处理
    def __init__(self,text = '请传入文字', mode = 'b'):
        #preset
        self.text = text
        self.mode = mode
        self.mode_list = {
            'm': 'mixed',
            'b': 'tts_baidu.TTSBaidu()',
            'g': 'tts_google.TTSGoogle()',
            'o': 'tts_offline.TTSOffline()'
        }
        self.max_size = 20
        #store data
        self.text_parts = []
        self.audio_parts = []
    def split_text(self):
        """
        Split text based on basic roman punctuation.
        If any the split fragment is still too long, cut the text fragment into short fragment up to length max_size.
        """
        punc = u'， “”《》〈〉！：；？（）【】‘’、{ } ——。"¡!()[]¿?.,;—«»\n'#super蛋疼的python字符串编码问题
        punc_list = [re.escape(c) for c in punc]
        pattern = '|'.join(punc_list)
        reg = re.compile(pattern.encode('utf-8'))
        raw_parts = reg.split(self.text)
        raw_parts = [item for item in filter(lambda x:x != '', raw_parts)]#去除空串，防止引起百度API的501 - parameter error.
        self.text_parts = raw_parts
        # for f in raw_parts:
        #     self.text_parts += self.split_fragment(f)

    def split_fragment(self,fragment):
        fragment = fragment.decode('utf-8')
        if len(fragment)>self.max_size:
            return [fragment[:self.max_size].encode('utf-8')] + self.split_fragment(fragment[self.max_size:])
        else:
            return [fragment.encode('utf-8') + ',']

    def show_text_parts(self):
        for p in self.text_parts:
            print ''.join([p])

    def tts(self):
        tts = eval(self.mode_list[self.mode])
        for part in self.text_parts:
            index = self.text_parts.index(part)
            self.audio_parts += [tts.text2audio(part,str(index))]#返回的是文件名，因为直接播放二进制mp3音频流没有找到实现方法
            print part, time.ctime()

    def begin_tts(self):
        self.split_text()
        self.show_text_parts()
        t = threading.Thread(target=self.tts, name='tts_thread')
        t.start()
        i = 0
        while True:
            if i<len(self.audio_parts):
                # a=os.system('ffplay -showmode 0 -autoexit %s.mp3'%i + "> /dev/null 2>&1")
                p = subprocess.Popen('ffplay -showmode 0 -autoexit %s'%self.audio_parts[i] + "> /dev/null 2>&1",shell=True)
                p.wait()
                i += 1
            else:
                if not t.is_alive():
                    # time.sleep(5)#让最后的一片段语音播放完毕
                    break
                time.sleep(0.5)

if __name__ == '__main__':
    text = '儿童安全座椅是一种系于汽车座位上,供儿童乘坐且有束缚设备并能在发生车祸时,束缚着儿童以最大限度保障儿童安全的座椅。;'
    tts_manger = TTSManger()
    tts_manger.text = text
    tts_manger.begin_tts()
