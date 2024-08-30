import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pyecharts import options as opts
from pyecharts.charts import Bar, Line

df = pd.read_excel('./销售数据明细.xlsx')

print(df.head())

print(df.isna().sum())

# 计算指标设定，设置本文需要计算的指标，指标计算如下：
#  收入=销量*销售额
#  单量=销量汇总
#  货品数=货品数去重
#  收入环比：本月收入/上月收入-1
#  单量环比：本月单量/上月单量-1

# 计算12.1到12.25的数据
# the_month = df[(df['销售日期'] >= datetime(2021,12,1)) & (df['销售日期'] <= datetime(2021,12,25))]
# revenue = (the_month['销量'] * the_month['销售额']).sum()    # 本月收入
# daily_revenue = the_month['销量'].sum()   # 单日单量
# goods = the_month['货号'].nunique()   # 本月的货品数
# print(f'本月收入：{revenue},单日单量：{daily_revenue},本月货品数：{goods}')

start_date1 = pd.to_datetime('2021-12-01')
end_date1 = pd.to_datetime('2021-12-25')

start_date2 = pd.to_datetime('2021-11-01')
end_date2 = pd.to_datetime('2021-11-25')
# 设置时间段
month1 = df[(df['销售日期'] >= start_date1) & (df['销售日期'] <= end_date1)]
month2 = df[(df['销售日期'] >= start_date2) & (df['销售日期'] <= end_date2)]


def get_month_data(df):
    revenue = (df['销量'] * df['销售额']).sum()
    daily_revenue = df['销量'].sum()
    goods = df['货号'].nunique()
    return revenue, daily_revenue, goods


revenue, daily_revenue, goods = get_month_data(month1)
revenue2, daily_revenue2, goods2 = get_month_data(month2)

print(f'12月收入：{revenue}, 单日单量：{daily_revenue}, 本月货品数：{goods}')
print(f'11月收入：{revenue2}, 单日单量：{daily_revenue2}, 本月货品数：{goods2}')

# 计算环比
ribao = pd.DataFrame({'12月': [revenue, daily_revenue, goods],
                      '11月': [revenue2, daily_revenue2, goods2]},
                     index=['收入', '单量', '货品数'])

ribao['环比'] = ribao['12月'] / ribao['11月'] - 1
ribao['环比'] = ribao['环比'].apply(lambda x: format(x, '.2%'))

print(ribao)

# 每月销售额、销量
df['销售月份'] = df['销售日期'].astype(str).str[0:7]
df_group = df.groupby('销售月份').aggregate({'销售额': 'sum', '销量': 'sum'})

print(df_group)

v1 = df_group['销售额'].tolist()
v2 = df_group['销量'].tolist()

bar = (Bar()
       .add_xaxis(df_group.index.tolist())
       .add_yaxis('销售额', v1, category_gap='50%', gap='6%')
       .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter='{value} 单'),min_=0,max_=1750))
       .set_series_opts(label_opts=opts.TitleOpts(is_show=True),color='skyblue')
       .set_global_opts(title_opts=opts.TitleOpts(title='21年每月销售额与销量'))
       )

line = (Line()
        .add_xaxis(df.index.tolist())
        .add_yaxis('销售量',v2,yaxis_index=1,is_smooth=True)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True),linestyle_opts=opts.LineStyleOpts(width=2))
        )


bar.overlap(line)

bar.render('21年每月销售额与销量.html')

