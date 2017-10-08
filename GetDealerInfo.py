#coding: utf8
from urllib.request import urlopen
import json
def getname(*id):

    Idlist = '|'.join(id)
    with urlopen('http://k.autohome.com.cn/frontapi/GetDealerInfor?dearerandspecIdlist='+Idlist,timeout=5) \
            as res:

        dealerlist =[]
        html = res.read().decode('gbk')
        jd =json.loads(html)
        for dealer in jd['result']['List']:
            dealerlist.append(dealer['CompanySimple'])

        # 完整的经销商信息 {'DealerId': 127165, 'Url': 'http://dealer.autohome.com.cn/127165/spec_25855.html',
            #  'CountryName': '巴南', 'ProvinceName': '重庆', 'SpecId': 25855, 'CityName': '重庆', 'CompanySimple':
            # '重庆合翘奔驰'}
    return dealerlist[0]

