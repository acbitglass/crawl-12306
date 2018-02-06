from flask import Flask
from flask import request
import requests
import time


def get_html(cz, cc):
    cz1 = str(cz.encode('GBK')).replace('\\x', '%')[1:].replace("'", "").upper()
    czEn = str(cz.encode('utf-8')).replace('\\x', '-')[1:].replace("'", "").upper()
    rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    tp = int(round(time.time() * 1000))

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'route=9036359bb8a8a461c164a04f8f50b252;BIGipServerotn=4124508426.64545.0000;RAIL_EXPIRATION'
                  '=1517334856976;RAIL_DEVICEID=c45tjwB5jIxQPfinovWlev0-FfoOh2gIJVt0KbnuDzBupe504MqiodF'
                  'bUU7o6g3HNmyfh2JCnyT5rDP8g7CHhsAsjdw9cETAJpKXo0Uhn3uA4HZ8XqTnWToFpHQtAvLtSqAbQy5fnHpeZS'
                  '-nV3sAAcQvAqOwUefg;BIGipServerzwdcx=4010803466.28695.0000;BIGipServerportal=3168010506.17695.'
                  '0000;JSESSIONID=h1STqvhwT2hT7nmqk3DhGF21mn7JMqJJy8s25xSqkpJ86JTTmh7l!-1818935495',
        'Host': 'dynamic.12306.cn',
        'Referer': 'http://dynamic.12306.cn/mapping/kfxt/zwdcx/LCZWD/CCCX.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_13_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome'
                  '/63.0.3239.132 Safari/537.36',
    }
    url = 'http://dynamic.12306.cn/mapping/kfxt/zwdcx/LCZWD/cx.jsp?cz=%s&cc=%s&cxlx=0&rq=%s&czEn=%s&tp=%s' % (cz1, cc, rq, czEn, tp)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>火车正晚点查询</h1>'


@app.route('/chaxun', methods=['GET'])
def chaxun_form():
    return '''<form action="/chaxun" method="post">
              <p><b>车&nbsp;&nbsp;&nbsp;站：</b><input name="cz"></p>
              <p><b>车&nbsp;&nbsp;&nbsp;次：</b><input name="cc"></p>
              <p><button type="submit">查 询</button></p>
              </form>'''


@app.route('/chaxun', methods=['POST'])
def chaxun():
    return get_html(request.form['cz'], request.form['cc'])


if __name__ == '__main__':
    app.run()
