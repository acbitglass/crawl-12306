import hmac
import json
import requests
import time
from hashlib import sha1


# 处理验证码
def get_captcha(data, need_cap):
    if need_cap is False:
        return
    with open('captcha.gif', 'wb') as fb:
        fb.write(data)
    return input('captcha:')


# 处理签名
def get_signature(grantType, clientId, source, timestamp):
    hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1)
    hm.update(str.encode(grantType))
    hm.update(str.encode(clientId))
    hm.update(str.encode(source))
    hm.update(str.encode(timestamp))
    return str(hm.hexdigest())


# 处理登录
def login(oncaptcha, sessiona, headers):
    type_username = input('请输入用户名:')
    type_password = input('请输入密码:')
    resp1 = sessiona.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn',
                         headers=headers)  # 拿cookie:capsion_ticket
    need_cap = json.loads(resp1.text)["show_captcha"]  # {"show_captcha":false} 表示不用验证码

    grantType = 'password'
    clientId = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    timestamp = str((time.time() * 1000)).split('.')[0]  # 签名只按这个时间戳变化

    captcha_content = sessiona.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
                                   headers=headers).content

    data = {
        "client_id": clientId,
        "grant_type": grantType,
        "timestamp": timestamp,
        "source": source,
        "signature": get_signature(grantType, clientId, source, timestamp),  # 获取签名
        "username": type_username,
        "password": type_password,
        "lang": "cn",
        "captcha": oncaptcha(captcha_content, need_cap),  # 获取图片验证码
        "ref_source": "other_",
        "utm_source": ""
    }

    resp = sessiona.post('https://www.zhihu.com/api/v3/oauth/sign_in', data, headers=headers).content

    return resp


if __name__ == "__main__":
    sessiona = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
               'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
    while 1:
        content = login(get_captcha, sessiona, headers)
        content = dict(json.loads(content))
        if 'error' in content.keys():
            print(content['error']['message'])
        else:
            resp = sessiona.get('https://www.zhihu.com/inbox', headers=headers)  # 登录进去了，可以看私信了
            print(resp.text)
            break
