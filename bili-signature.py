#导入依赖
from colorama import *
import datetime
import json
import random
import requests
from rpnpy import Calculator
import signal
from time import sleep


class BilibiliApi(object):
    #调试模式
    debug = False
    debugFans = 1984

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
        self.getFansUrl = 'https://api.bilibili.com/x/web-interface/nav/stat'
        self.setSignatureUrl = 'https://api.bilibili.com/x/member/web/sign/update'
        self.initHeaders(sessdata, bilijct)
    
    #初始化Headers
    def initHeaders(self, sessdata, bilijct):
        cookies = 'SESSDATA=%s; bili_jct=%s' % (sessdata, bilijct)
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
        if (response['code'] != 0):
            print('粉丝数获取错误')
            exit()
        return response['data']['follower']

    #修改账号个人简介
    def setSignature(self):
        return requests.post(url=self.setSignatureUrl, params=self.params, headers=self.headers, timeout=10)

#配置文件管理
class config(object):
    #初始化配置
    def initConfig(self):
        try:
            with open('./config.json','r',encoding='utf8') as fp:
                data = json.load(fp)
                fp.close()
                return data
        except Exception:
            print('文件读取失败')
            exit()
    
    def __init__(self):
        self.config = self.initConfig()

#获取当前时间字符串
def getCurrTime():
    nowTime = datetime.datetime.now()
    return nowTime.strftime('%m-%d-%H:%M:%S')

#符号转为比大小
def compare(symbol, a, b):
    if symbol == '>=':
        return a >= b
    elif symbol == '>':
        return a > b
    elif symbol == '<=':
        return a <= b
    elif symbol == '<':
        return a < b
    elif symbol == '=':
        return a >= b
    else: 
        print('json解析错误')
        exit()

#个人简介处理
class Signature(object):
    def __init__(self, cfg):
        self.basic = cfg['signature']
        self.cfg = cfg['advanced']

    #计算逆波兰表达式
    def processRPN(self, input):
        calc = Calculator()
        calc.execute(input)
        (result,) = calc.stack
        return result

    #获取简介
    def getSignature(self, fans):
        cfg = self.cfg
        if (not cfg['enabled']):
            return self.basic % (fans + 1)
        else:
            return self.getSignature2(fans, cfg)

    #获取简介2，真正的获取简介，支持套娃
    def getSignature2(self, fans, cfg):
        processedRPN = self.processRPN(cfg['RPN'] % fans)
        if (compare(cfg['type'], processedRPN, cfg['value'])):
            if 'tw' in cfg['ifTrue']:
                return self.getSignature2(fans, cfg['ifTrue']['tw'])
            if cfg['ifTrue']['formatted'] == True:
                return cfg['ifTrue']['text']
            else:
                RPNResult = self.processRPN(cfg['ifTrue']['RPN'] % fans)
                return cfg['ifTrue']['text'] % RPNResult
        else:
            if 'tw' in cfg['ifFalse']:
                return self.getSignature2(fans, cfg['ifFalse']['tw'])
            if cfg['ifFalse']['formatted'] == True:
                return cfg['ifFalse']['text']
            else:
                RPNResult = self.processRPN(cfg['ifFalse']['RPN'] % fans)
                return cfg['ifFalse']['text'] % RPNResult

#Ctrl+C处理       
def _exit(signum, frame):
    print('停止中...')
    exit()
signal.signal(signal.SIGINT, _exit)
signal.signal(signal.SIGTERM, _exit)

'''主程序入口'''
if __name__ == '__main__':
    #打印介绍
    print(rf"""        {Fore.LIGHTMAGENTA_EX}╭──────────────────────────────────────────────────────────────────────╮
        | {Fore.LIGHTCYAN_EX}哔哩哔哩自动更改个人简介 原作者: wuziqian211 二改者: ThebestkillerTBK{Fore.LIGHTMAGENTA_EX}| 
        | {Fore.LIGHTCYAN_EX}本程序可以根据自己的哔哩哔哩账号的粉丝数，自动更改您的个人简介。     {Fore.LIGHTMAGENTA_EX}| 
        ╰──────────────────────────────────────────────────────────────────────╯{Style.RESET_ALL}""")
    cfg = config().config
    api = BilibiliApi(cfg['SESSDATA'], cfg['bili_jct'])
    sign = Signature(cfg)
    if (cfg['freq'] < 15):
        print('时间太短了:3')
        exit()
    
    #调试模式，用来测试高级模式
    if api.debug:
        fans = api.debugFans
        _sign = sign.getSignature(fans)
        print('当前粉丝数: %d, 将要设置签名 %s' % (fans, _sign))
        exit()

    #主循环
    while(1):
        fans = api.getFans()
        if (fans != api.getLastFans()):
            _sign = sign.getSignature(fans)
            api.initParams(sign, cfg['SESSDATA'], cfg['bili_jct'])
            print('[%s]当前粉丝数: %d, 将要设置签名 %s' % (getCurrTime(), fans, _sign))
            res = api.setSignature().text
            print('[%s]当前粉丝数: %d, 返回: %s' % (getCurrTime(), fans, res))
            api.setLastFans(fans)
        sleep(cfg['freq'] + random.randint(3, 10))
