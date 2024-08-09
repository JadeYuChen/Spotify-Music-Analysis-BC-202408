#用箱型图进行可视化
import pandas as pd
import plotly.express as px
import plotly.io as pio

#定义需要呈现的指标
columns = ["Release Date", "Length (ms)", "Popularity", "Key", "Mode", "Danceability", "Acousticness", 
           "Energy", "Instrumentalness", "Liveness", "Loudness", "Speechiness", 
           "Tempo", "Time Signature", "Valence"]

#定义想要比较的国家
regions = ["usa", "japan", "united kingdom", "germany", "china", "france", "south korea", "canada", "brazil", "australia"]

#加载所有数据到一个DataFrame中
all_data = []
for region in regions:
    df = pd.read_csv(f"{region}_top50_tracks.csv")
    df['Region'] = region.capitalize()  # 添加地区列
    all_data.append(df)

#合并所有地区的数据
all_df = pd.concat(all_data)

#绘制每个指标的箱型图
for column in columns:
    fig = px.box(all_df, x='Region', y=column, title=f'Comparison of {column} across Regions')

     #修改标题字体格式
    fig.update_layout(
        title={
            'text': f'Comparison of {column} across Regions',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, family='Arial', color='black', weight='bold')  # 字体设置
        }
    )
    fig.show()

    fig.write_html(f"result/{column}_comparison_box_plot.html")
    fig.write_image(f"result/{column}_comparison_box_plot.png")

