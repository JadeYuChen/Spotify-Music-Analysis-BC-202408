import pandas as pd
import plotly.express as px

columns = ["Release Date", "Length (ms)", "Popularity", "Key", "Mode", "Danceability", "Acousticness", 
           "Energy", "Instrumentalness", "Liveness", "Loudness", "Speechiness", 
           "Tempo", "Time Signature", "Valence"]

regions = ["usa", "japan", "united kingdom", "germany", "china", "france", "south korea", "canada", "brazil", "australia"]

all_data = []
for region in regions:
    df = pd.read_csv(f"{region}_top50_tracks.csv")
    df['Region'] = region.capitalize()  # 添加地区列
    df['Rank'] = df.index + 1  # 添加排名列
    all_data.append(df)

all_df = pd.concat(all_data)


#绘制散点图
for column in columns:
    fig = px.scatter(all_df, x='Rank', y=column, color='Region', 
                     title=f'Comparison of {column} across Regions',
                     color_discrete_sequence=px.colors.qualitative.Light24
                     )
    
    fig.update_layout(
        title={
            'text': f'Comparison of {column} across Regions',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top', 
            'font': dict(size=20, family='Arial', color='white', weight='bold')
        },
        plot_bgcolor='#130B60',
        font_color='white', 
        paper_bgcolor='#130B60'
    )

    fig.update_xaxes(linecolor='white', gridcolor='#130B60', zeroline=False)
    fig.update_yaxes(linecolor='white', gridcolor='#130B60', zeroline=False)
    
    fig.show()
    
    fig.write_html(f"result/{column}_comparison_scatter_plot.html")
    fig.write_image(f"result/{column}_comparison_scatter_plot.png")
