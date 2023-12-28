import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
info_data = pd.read_csv("moviesInfo.csv")
df = info_data
# 各年份上映电影数量
df[["year", "month", "day"]] = df["release_date"].str.split("-", expand=True)
df['year'] = df['year'].astype("int")
year_counts = df['year'].value_counts()
c = (
    Bar()
    .add_xaxis(list(year_counts.index))
    .add_yaxis('上映数量', year_counts.values.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title='各年份上映电影数量'),
        yaxis_opts=opts.AxisOpts(name='上映数量'),
        xaxis_opts=opts.AxisOpts(name='上映年份'),
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_='inside')],)
    .render('各年份上映电影数量.html')
)

# 电影时长前十
df[["min", "other"]] = df["runtime"].str.split("分钟", expand=True)
df['min'] = df['min'].astype("int")
df.sort_values('min', inplace=True)
b = (
    Bar()
    .add_xaxis(df['film_name'].values.tolist()[-10:])
    .add_yaxis('片长', df['min'].values.tolist()[-10:])
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='电影时长前十排行'),
        yaxis_opts=opts.AxisOpts(name='片名'),
        xaxis_opts=opts.AxisOpts(name='时长/min'),
        datazoom_opts=opts.DataZoomOpts(type_='inside'),
    )
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .render('电影时长前十排行.html')
)
# 电影评价人数前二十
df['rating_people'] = df['rating_people'].astype("int64")
df.sort_values('rating_people', inplace=True)
c = (
    Bar()
    .add_xaxis(df['film_name'].values.tolist()[-20:])
    .add_yaxis('评价人数', df['rating_people'].values.tolist()[-20:])
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='评价人数前二十电影排行'),
        yaxis_opts=opts.AxisOpts(name='片名'),
        xaxis_opts=opts.AxisOpts(name='人数/个'),
        datazoom_opts=opts.DataZoomOpts(type_='inside'),
    )
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .render('评价人数前二十电影排行.html')
)
