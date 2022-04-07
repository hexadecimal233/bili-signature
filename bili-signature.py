#导入依赖
from colorama import *
import datetime
import json
import random
import requests
from rpnpy import Calculator
import signal
from sys import exit
from time import sleep

VERSION = '2.2'

class BilibiliApi(object):
    #调试模式
    debug = False
    debugFans = 1994

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
class Config(object):
    #初始化配置
    def initConfig(self):
        try:
            with open('./config.json','r',encoding='utf8') as fp:
                data = json.load(fp)
                fp.close()
                return data
        except Exception:
            print('配置读取失败,请确保你已将config.json.template重命名为config.json')
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
        print('解析错误')
        exit()

#个人简介处理
class Signature(object):
    def __init__(self, cfg):
        self.basic = cfg['signature']
        self.advancedMode = cfg['advancedMode']
        self.advancedCfg = cfg['advanced']

    #计算逆波兰表达式
    def processRPN(self, input):
        calc = Calculator()
        calc.execute(input)
        (result,) = calc.stack
        return result

    #获取简介
    def getSignature(self, fans):
        if (not self.advancedMode):
            return self.basic % (fans + 1)
        else:
            return self.getSignature2(self.advancedCfg, fans)

    #格式化签名
    def getText(self, condition, cfg, fans):
        currCFG = cfg[condition]
        return self.getText2(currCFG, fans)

    #真正格式化签名
    def getText2(self, cfg, fans):
        if 'tw' in cfg:
            return self.getSignature2(cfg['tw'], fans)
        if 'data' in cfg:
            return self.getText2(cfg['data'][random.randint(0, len(cfg['data'])-1)], fans)
        if cfg['formatted'] == True:
            return cfg['text']
        else:
            RPNResult = self.processRPN(cfg['RPN'] % fans)
            return cfg['text'] % RPNResult
    
    #解析条件
    def parseCriteria(self, cfg, fans):
        if 'time' in cfg:
            timeCfg = cfg['time']
            compared = datetime.datetime.strptime(timeCfg['time'],'%H:%M')
            nowDaytime = datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M'),'%H:%M')
            cond = compare(timeCfg['type'], nowDaytime, compared)
            time_ = cond
        else: time_ = 1
        if 'date' in cfg:
            timeCfg = cfg['date']
            compared = datetime.datetime.strptime(timeCfg['date'],'%Y-%m-%d')
            nowDate = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
            cond = compare(timeCfg['type'], nowDate, compared)
            date_ = cond
        else: date_ = 1
        if 'fans' in cfg:
            fansCfg = cfg['fans']
            fans_ = self.parseFansType(fansCfg['RPN'], fansCfg['type'], fansCfg['value'], fans)
        else: fans_ = 1

        return (fans_ and time_ and date_)

    #解析粉丝
    def parseFansType(self, RPN, criteria, value, fans):
        processedRPN = self.processRPN(RPN % fans)
        return compare(criteria, processedRPN, value)
            
    #获取简介2，真正的获取简介，支持套娃
    def getSignature2(self, cfg, fans):
        if (self.parseCriteria(cfg['criteria'], fans)):
            return self.getText('ifTrue', cfg, fans)
        else:
            return self.getText('ifFalse', cfg, fans)

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
        ╰──────────────────────────────────────────────────────────────────────╯
                                        V{VERSION}{Style.RESET_ALL}""")
    cfg = Config().config
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
