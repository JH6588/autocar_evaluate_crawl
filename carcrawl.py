# coding: utf8
import requests
from bs4 import BeautifulSoup
from coment_extract import deal_comment_text
from GetDealerInfo import getname
import store_config
from multiprocessing.dummy import Pool
from queue import Queue
import threading
from urllib.request import urlopen
from pymysql import connect
import sys

# import socket

# socket.setdefaulttimeout(20)
sys.stdout = open('logerr.txt', 'w')


def get_car_box():
    # c = get_comment()
    # c.__next__()
    res = requests.get('http://k.autohome.com.cn/suva01/')
    bs = BeautifulSoup(res.text, 'html.parser')
    for car in bs.select('div.findcont-choose a'):
        lx = 'http://k.autohome.com.cn' + car['href']
        bsj = BeautifulSoup(requests.get(lx).text, 'html.parser')
        car_domain = 'http://k.autohome.com.cn'
        for car in bsj.select('.cont-name a'):

            bs = BeautifulSoup(requests.get(car_domain + car['href']).text, 'html.parser')

            if bs.select('a.page-item-last'):
                page_info = bs.select('a.page-item-last')[0]['href'].split('/')
                # print(page_info)
                # 比如网站 http://k.autohome.com.cn/874/， page_num 为总评论页数
                # page_id =page_info[1]
                page_num = page_info[2][6:-5]
            else:
                page_num = 1
            page_id = car['href']

            comment_page = ('http://k.autohome.com.cn{}index_{}.html'.format(page_id, j) for j in
                            range(15, int(page_num) + 1))
            print(comment_page)
            for page in comment_page:
                yield page


def get_comment(lx):
    with urlopen(lx, timeout=30) as res:
        bsj = BeautifulSoup(res.read().decode('gbk', 'ignore'), 'html.parser')
        for div in bsj.select('div.mouthcon'):
            # div =bsj.select('div.mouthcon')[5]
            # 通过键值对 对应关系 确定item 的key 和value 可以避免不同页面直接 字段不同步 造成的报错
            item = {}
            try:
                comment_id = div.select('div[id^=divfeeling]')[0]['id'][11:]
                item.update(deal_comment_text(comment_id))
                field_list = [''.join(ele.text.split()) for ele in
                              div.select('div.choose-con.mt-10 > dl.choose-dl > dt')]
                cont_list = [''.join(ele.text.split()) for ele in
                             div.select('div.choose-con.mt-10 > dl.choose-dl > dd')]
                item.update(dict(zip(field_list, cont_list)))
                field_star_list = [ele.text.strip() + u'评分' for ele in div.select('div.position-r  dt')]
                info_star_list = [ele.text.strip() for ele in div.select('.position-r dl > dd > span.font-arial.c333')]
                item.update(dict(zip(field_star_list, info_star_list)))
            except:
                continue

            try:
                item[u'主题'] = div.select('div.cont-title.fn-clear > div > a')[0].text
            except:
                item[u'主题'] = ''

            if u'购车经销商' in item.keys():
                id = div.select('a[data-val]')[0].get('data-val')
                try:
                    item[u'购车经销商'] = getname(id)
                except:
                    item[u'购车经销商'] = ''

            if u'油耗目前行驶' in item.keys():
                item[u'油耗参数'] = item[u'油耗目前行驶'].split(u'公里')[0] + u'公里'
                item[u'目前行驶'] = item[u'油耗目前行驶'].split(u'公里')[1] + u'公里'
                del item[u'油耗目前行驶']

            if u'购买车型' in item.keys():
                try:
                    c = item[u'购买车型'].index(u'款')  # 用款来做切割点
                    item[u'品牌'] = item[u'购买车型'][:c - 4]
                    item[u'车型'] = item[u'购买车型'][c - 4:]
                except:
                    item[u'品牌'] = item[u'购买车型']
                finally:
                    del item[u'购买车型']

            key_list = ['外观', '动力', '空间', '油耗', '裸车购买价', '车型', '目前行驶', '其他描述', '舒适性',
                        '购买时间', '购买地点', '主题', '操控', '购车目的', '内饰', '为什么最终选择这款车',
                        '性价比', '油耗参数', '购车经销商']
            for k in key_list:
                if k not in item.keys():
                    item[k] = ''
            col = ','.join(item.keys())
            try:
                conn = connect(user='root', password='123', database='test3', charset='utf8mb4')
                cur = conn.cursor()
                cur.execute(
                    'insert into carcoment6({}) values( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'
                    '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(
                        col), list(item.values()))
                # print(comment_id)
            except:
                # print(lx,'\n')
                print(item)  # 方便确定错误
                continue
            finally:
                conn.commit()


class Coment(threading.Thread):
    def __init__(self, Queue):
        threading.Thread.__init__(self)
        self.Queue = Queue

    def run(self):
        while True:
            lx = self.Queue.get()
            get_comment(lx)
            self.Queue.task_done()


if __name__ == '__main__':

    q = Queue()
    for i in range(10):
        c = Coment(q)
        c.daemon = True
        c.start()

    for link in get_car_box():
        q.put(link)

    q.join()
    print('ok ,done!')
