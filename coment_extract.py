#coding: utf8
import re
from urllib.request import urlopen
import json


#a = '【最满意的一点】颜值高，油耗。【最不满意的一点】副驾无电动，三十万的车舒适感谈不上。
# 【空间】空间都说小我觉得还好，两口之家非常合适，本人身高175位置调好还好，说不上顶头。
# 【动力】完全够用，主要是老婆用。0-100实测12s。自动模式，没试过手动。1.2档有点勉强，后面还是比较给力，超车还是没有压力。
# 【操控】操控精准，驾驶很舒服，怀档逼格也是够。
# 【油耗】目前7.7个油3000公里。非常满意，高速7个不到。城里很少去，具体没测。
# 【舒适性】这
# 就得好好吐槽了，乘坐舒适度一般，做工材质来说谈不上好吧，感觉上没我以前高尔夫舒适，毕竟是奔驰，实话实说有待提高。
# 重点说说胎噪，
# 防爆胎确实噪音大，高速特别明显，准备换普通轮胎了。
# 【外观】就是因为外观买的这款车，主要是钙蓝??，超爱！！！
# 【内饰】
# 内饰非常满意，材质一般般
# 【性价比】为了现车钙蓝也是多了点钱，白色现车多，感觉白g确实已经烂大街了。总得说还能接受。
# 【为什么最终选择这款车？】颜值，因为以前在小区门口看到一个新车，而且就是gla钙蓝，就钟情这款车，而且选到了心仪的颜色.
# 【其它描述】'



def deal_comment_text(id):
    with urlopen('http://k.autohome.com.cn/FrontAPI/GetFeelingByEvalId?evalId={}'.format(id)) as res:
        tx =res.read().decode('gbk','ignore')
        try:
            tx=json.loads(tx).replace('<br/>','')  #消除一些符号的unicode 字符
        except:
            pass
        field_list = [ele   for ele in re.findall(u'【(.*?)】',tx)]
        comment_info =[ele for ele in re.findall(u'】(.*?)【|$',tx)]
        for i in   range(len(field_list)):
            if '其它' in field_list[i]:
                field_list[i] ='其他描述'
            if '为什么' in field_list[i]:
                field_list[i] ='为什么最终选择这款车'
            if '【' or '】' in field_list[i]:
                field_list[i] =re.sub('【|】','',field_list[i])

        return dict(zip(field_list,comment_info))







