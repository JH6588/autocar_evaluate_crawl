from pandas.io.api import read_excel
import pandas as pd
import matplotlib.pyplot as plt
qiche = read_excel(r'C:\Users\hui\Desktop\carcoment6.xlsx')
qiche.裸车购买价=qiche.裸车购买价.str.replace('万元', '').astype('float')
prize=qiche.裸车购买价
qc=qiche[(prize> 12) & (prize < 18)]   #通过价格 筛选 这里是12到 18万之间的 ，可更改

grade =pd.Series(qc.油耗评分 +qc.动力评分+qc.操控评分+qc.内饰评分+qc.性价比评分+qc.外观评分+qc.动力评分+qc.舒适性评分)
#将分数求和 聚类成新的字段grade
car = pd.DataFrame({'brand':qc.品牌,'prize':qc.裸车购买价,'grade':grade})
group_car = car.groupby(by='brand').sum()/car.groupby(by='brand').count()
pivot_car =pd.pivot_table(car,index=['brand',])
che  =pivot_car.sort_values(by='grade',ascending=False)
#写入本地excel
writer= pd.ExcelWriter('che.xlsx')
che.to_excel(writer)
writer.save()
#直方图
plt.hist2d(che.grade,che.prize,bins=7,normed=False) 
plt.show()
