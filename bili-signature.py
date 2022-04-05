#导入依赖
import datetime
import json
import random
import requests
from colorama import *
from time import sleep

class BilibiliApi(object):
    #上一粉丝数
    __fans = 0

    @classmethod
    def getLastFans(cls):
        return cls.__fans

    @classmethod
    def setLastFans(cls, num):
        cls.__fans = num

    # api地址
    def __init__(self, sessdata, bilijct):
        self.getFansUrl = 'http://api.bilibili.com/x/web-interface/nav/stat'
        self.setSignatureUrl = 'https://api.bilibili.com/x/member/web/sign/update'
        self.initHeaders(sessdata, bilijct)
    
    #初始化Headers
    def initHeaders(self, sessdata, bilijct):
        cookies = "SESSDATA=%s; bili_jct=%s" % (sessdata, bilijct)
        self.headers = {
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
    
    #初始化Post参数
    def initParams(self, signature, sessdata, bilijct):
        self.params = {
            'user_sign': signature,
            'csrf': bilijct,
            'SESSDATA': sessdata
        }

    #获取账号粉丝数
    def getFans(self):
        response = requests.get(url=self.getFansUrl, headers=self.headers, timeout=10).json()
        followers = response['data']['follower']
        if (followers == -1):
            raise Exception(ValueError, '粉丝数获取错误')
        return followers

    #修改账号个人简介
    def setSignature(self):
        return requests.post(url=self.setSignatureUrl, params=self.params, headers=self.headers, timeout=10)

class config(object):
    #初始化配置
    def initConfig(self):
        with open('./config.json','r',encoding='utf8') as fp:
            data = json.load(fp)
            fp.close()
            return data
    
    def __init__(self):
        self.config = self.initConfig()

def getCurrTime():
    nowTime = datetime.datetime.now()
    return nowTime.strftime('%m-%d-%H:%M:%S')

if __name__ == '__main__':
    print(rf"""
        {Fore.LIGHTMAGENTA_EX}╭─────────────────────────────────────────────────────────────────────╮
        | {Fore.LIGHTCYAN_EX}哔哩哔哩自动更改个人简介 原作者: wuziqian11 二改者: ThebestkillerTBK{Fore.LIGHTMAGENTA_EX}| 
        | {Fore.LIGHTCYAN_EX}本程序可以根据自己的哔哩哔哩账号的粉丝数，自动更改您的个人简介。    {Fore.LIGHTMAGENTA_EX}| 
        ╰─────────────────────────────────────────────────────────────────────╯
    """)
    print(Style.RESET_ALL)
    cfg = config().config
    api = BilibiliApi(cfg['SESSDATA'], cfg['bili_jct'])
    if (cfg['freq'] < 30):
        raise Exception(ValueError, '时间太短了，不行')
    while(1):
        fans = api.getFans()
        if (fans != api.getLastFans()):
            sign = cfg['signature'] % (fans + 1)
            api.initParams(sign, cfg['SESSDATA'], cfg['bili_jct'])
            print("[%s]当前粉丝数: %d, 将要设置签名 %s" % (getCurrTime(), fans, sign))
            res = api.setSignature()
            print("[%s]当前粉丝数: %d, 返回: %s" % (getCurrTime(), fans, res.text))
            api.setLastFans(fans)
        sleep(cfg['freq'] + random.randint(3,10))
