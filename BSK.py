import base64
import json
import math
import random
import time
import urllib
from urllib.parse import urlencode

import requests

proxies = {"http": None, "https": None}

postPayload = {
    'ie': 'utf-8',
    'kw': 'peekspsi',
    'fid': 111,  # 吧id
    'tid': 111,  # 贴子id
    'vcode_md5': '',
    'floor_num': 1,
    'rich_text': 1,
    'tbs': '',
    'content': 'p',
    'basilisk': 1,
    'files': '[]',
    'mouse_pwd': '',
    'mouse_pwd_t': 1,
    'mouse_pwd_isclick': 1,
    'nick_name': '昵称',
    '__type__': 'reply',
    '_BSK': 'bsk',
    'geetest_success': 0,

}
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "tieba.baidu.com",
    "Origin": "https://tieba.baidu.com",
    "Pragma": "no-cache",
    "Referer": "https://tieba.baidu.com/p/7236785775",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.198 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
cookies = {
    "BDUSS": "----"
}

BSK_orig = {"a1": 1536,  # screen_availWidth
            "a2": 834,  # screen_availHeight
            "a3": False,  # window.document.body.addBehavior
            "a4": False,  # awesomium检测 False
            "c1": True,  # canvas
            "d1": "NULL",  # doNotTrack
            "e1": 20170511,  # global.process.type || global.process.versions.electron
            "i1": True,  # indexedDB
            "k1": False,  # sendByKeyBoard
            "k2": "229,80,229",  # keyUpArr 键盘输入keycode记录 最大10个
            "l1": "zh-CN",  # language
            "l2": True,  # localStorage
            "m1": "basilisk_aLv0jg",
            "m2": "(312,6878),(307,6889),(262,6914),(248,6918),(238,6927),(180,6939),(173,6941),(216,6946),(206,"
                  "6949),(102,371)",  # mouseMoveArr 鼠标位置记录 最大10个
            "m3": True,  # isMouseClicked
            "m4": "0,6577.60009765625",  # scrollArr 滚动条位置记录 最大5个
            "m5": True,  # sendByClick
            "n1": 20170511,  # window.__nightmare 20170511
            "n2": True,  # global
            "n3": 20170511,  # global.process.versions
            "p1": "%7B%22tbs%22%3A%22ac1a4918034084c71614325079%22%7D",  # tbs urlencoded
            "p2": "Win32",  # platform
            "p3": False,  # window.phantom检测 False
            "r1": "function random() { [native code] }",
            "s1": 864,  # screen_height
            "s2": 1536,  # screen_width
            "s3": True,  # sessionStorage True
            "t1": "function toString() { [native code] }",
            "t2": 0,  # ts
            "u1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.198 Safari/537.36",
            "w1": "NULL",  # document_height
            "w2": "NULL",  # document_width
            "w3": False,  # selenium|webdriver检测 False
            "w4": "window,self,document,name,location,customElements,history,locationbar,menubar,personalbar,"
                  "scrollbars,statusbar,toolbar,status,closed,frames,length,top,opener,parent,frameElement",
            }

tbs = {"tbs": ""}


def getTs(_type):
    if _type == "s":
        return math.floor(time.time())
    if _type == "ms":
        return math.floor(time.time() * 1000)


def decodeBSK(_BSK_cipher, _tbs):
    result = ""
    for no, item in enumerate(base64.b64decode(_BSK_cipher)):
        result = result + chr(item ^ ord(tbs['tbs'][no % len(tbs['tbs'])]))
    return result


def encodeBSK(_BSK_original):
    _str = "{"
    for i in _BSK_original:
        "下面分情况是因为真实BSK原文里值是字符串的:后面没空格_(:з」∠)_"
        if type(_BSK_original[i]) == int:
            _str += '"' + i + '": '
            _str += str(_BSK_original[i]) + ','
        if type(_BSK_original[i]) == bool:
            _str += '"' + i + '": '
            if _BSK_original[i]:
                _str += "true" + ','
            elif not _BSK_original[i]:
                _str += "false" + ','
        if type(_BSK_original[i]) == str:
            _str += '"' + i + '":'
            _str += '"' + str(_BSK_original[i]) + '",'
    _str = _str[:-1] + '}'
    BSK_str = ""
    for no, item in enumerate(_str):
        BSK_str += chr(ord(item) ^ ord(tbs['tbs'][no % len(tbs['tbs'])]))
    BSK_str = base64.b64encode(BSK_str.encode(encoding='ascii')).decode(encoding='ascii')
    return BSK_str


"获取tbs"
tbs['tbs'] = json.loads(requests.get("http://tieba.baidu.com/dc/common/tbs", cookies=cookies).content)['tbs']
postPayload['tbs'] = tbs['tbs']
BSK_orig['p1'] = "%7B%22tbs%22%3A%22" + tbs['tbs'] + "%22%7D"


"随机mouse_pwd"
mouse_pwd = ""
for i in range(0, 43):
    mouse_pwd += str(random.randint(30, 60)) + ','
mouse_pwd = mouse_pwd

"有的人是时间末尾加0,有的是加1"
ts = getTs('ms') - 60000
mouse_pwd = mouse_pwd + str(ts) + "1"

postPayload['mouse_pwd'] = mouse_pwd
postPayload['mouse_pwd_t'] = ts


"BSK里面的随机鼠标轨迹和滚动轨迹"
moustr = ""
for i in range(0, 10):
    moustr += '(' + str(random.randint(600, 700)) + ',' + str(random.randint(6000, 6400)) + '),'
moustr = moustr[:-1]
# BSK_orig['m2'] = moustr

scostr = ""
for i in range(0, 4):
    scostr += str(6400 * random.random()) + ','
scostr = scostr[:-1]
# BSK_orig['m4'] = scostr

print(moustr)
print(scostr)

ts_s = getTs('s')
BSK_orig['t2'] = ts_s

postPayload['_BSK'] = encodeBSK(BSK_orig)

r = requests.post("https://tieba.baidu.com/f/commit/post/add", headers=headers, data=postPayload, cookies=cookies)

print("响应:",r.content)
print("BSK密文:", postPayload['_BSK'])
print("tbs:", tbs['tbs'])
# print(postPayload['mouse_pwd'], postPayload['mouse_pwd_t'])
# print(urlencode(postPayload))
# print(json.loads(urllib.parse.unquote(json.loads(decodeBSK(encodeBSK(BSK_orig), tbs))['p1']))['tbs'] == tbs['tbs'])
