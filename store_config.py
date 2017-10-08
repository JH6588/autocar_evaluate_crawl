# coding: utf8
from pymysql import connect

conn = connect(user='root', password='123', database='test3', charset='utf8mb4')
cur = conn.cursor()


tab_field = '''品牌 varchar(300) ,车型 varchar(200) , 购买地点 varchar(200),购车经销商 varchar(200), 
购买时间 varchar(200) , 裸车购买价 varchar(200) , 油耗 varchar(200) , 目前行驶  varchar(200) ,
空间评分 varchar(200) , 动力评分 varchar(200) , 操控评分 varchar(200) ,油耗评分 varchar(200) ,
 舒适性评分 varchar(200) , 外观评分 varchar(200) ,内饰评分 varchar(200) ,性价比评分 varchar(200) , 
 购车目的  varchar(500) , 主题 varchar(1000) ,动力 text , 为什么最终选择这款车 text , 最满意的一点 text ,
 舒适性 text , 操控 text , 内饰  text , 外观  text, 空间  text, 其他描述 text , 最不满意的一点  text , 
 性价比  text , 油耗参数 text'''

# print(len(tab_field.split(',')))
# item_key_list = ['裸车购买价', '购买地点', '油耗', '油耗评分', '购车目的', '最不满意的一点', '性价比评分',
# '内饰评分', '最满意的一点', '购买车型', '操控评分', '外观', '主题', '空间', '动力', '舒适性', '其他描述',
# '舒适性评分', '购买时间', '性价比', '为什么最终选择这款车？', '动力评分', '内饰', '目前行驶', '外观评分', '
# 操控', '空间评分']

cur.execute('create table if not exists carcoment6({})'.format(tab_field))
conn.commit()
conn.close()
