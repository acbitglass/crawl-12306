# 检测余票并提示
import json
from json.decoder import JSONDecodeError
from urllib.parse import urlencode
import re
import requests

baseurl = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?'
requests.packages.urllib3.disable_warnings()
urll = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
r = requests.get(urll, verify=False)
pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
context = re.findall(pattern, r.text)
station = dict(context)


def get_html(date1, h_from_station1, h_to_station1):
    from_station = station[h_from_station1]
    to_station = station[h_to_station1]
    data = {
        'leftTicketDTO.train_date': date1,
        'leftTicketDTO.from_station': from_station,
        'leftTicketDTO.to_station': to_station,
        'purpose_codes': 'ADULT',
    }
    url = baseurl + urlencode(data)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_html(pre_html):
    train_list = []
    html0 = json.loads(pre_html)['data']['result']
    for i in range(0, len(html0)):
        data_list = html0[i].split('|')
        train_number = data_list[3]
        from_station_code = data_list[6]
        from_station_name = list(station.keys())[list(station.values()).index(from_station_code)]
        to_station_code = data_list[7]
        to_station_name = list(station.keys())[list(station.values()).index(to_station_code)]
        from_time = data_list[8]
        to_time = data_list[9]
        time_needed = data_list[10]
        first_class_seat = data_list[31] or '--'
        second_class_seat = data_list[30] or '--'
        soft_sleep = data_list[23] or '--'
        hard_sleep = data_list[28] or '--'
        hard_seat = data_list[29] or '--'
        no_seat = data_list[26] or '--'
        msg = {
            '车次': train_number,
            '出发车站': from_station_name,
            '到达车站': to_station_name,
            '出发时间': from_time,
            '到达时间': to_time,
            '历时': time_needed,
            '一等座': first_class_seat,
            '二等座': second_class_seat,
            '软卧': soft_sleep,
            '硬卧': hard_sleep,
            '硬座': hard_seat,
            '无座': no_seat
        }
        train_list.append(msg)
    return train_list


def detet_ticket(info):
    L = []
    for train in info:
        if train['二等座'] != '--' and train['二等座'] != '无':
            print('车次%s二等座有余票%s张' % (train['车次'], train['二等座']))
            L.append('whatever')
        if train['硬座'] != '无' and train['硬座'] != '--':
            print('车次%s硬座有余票%s张' % (train['车次'], train['硬座']))
            L.append('whatever')
    if len(L) == 0:
        print('已无您所需要的车票')


if __name__ == '__main__':
    try:
        date = input('请输入日期:')
        h_from_station = input('请输入出发车站:')
        h_to_station = input('请输入到达车站:')
        # date = '2018-02-11'
        # h_from_station = '合肥'
        # h_to_station = '安庆西'
        pre_htmlone = get_html(date, h_from_station, h_to_station)
        html = parse_html(pre_htmlone)
        detet_ticket(html)
    except JSONDecodeError and KeyError:
        print('输入有误')
