import json
import requests

class BilibiliApi(object):
    def __init__(self):
        # api地址
        self.getFansUrl = 'http://api.bilibili.com/x/web-interface/nav/stat'
        self.setFansUrl = 'https://api.bilibili.com/x/member/web/sign/update'

    #获取粉丝数
    def getFans(self, sessdata, bilijct):
        cookies = "SESSDATA=%s; bili_jct=%s" % (sessdata, bilijct)
        headers = {
        'Cookie':cookies,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        response = requests.get(url=self.getFansUrl,headers=headers,timeout=10).json
        return response

class config(object):
    #初始化配置
    def initConfig(self):
        with open('./config.json','r',encoding='utf8') as fp:
            data = json.load(fp)
            fp.close()
            return data
    
    def __init__(self):
        self.config = self.initConfig()

if __name__ == '__main__':
    api = BilibiliApi()
    cfg = config().config
    sessdata = cfg['SESSDATA']
    bilijct = cfg['bili_jct']
    freq = cfg['freq']
    signature = cfg['signature']
    print(sessdata + bilijct + freq + signature)
    fans = api.getFans(sessdata,bilijct)
    