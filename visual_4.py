import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

regions = ["usa", "japan", "united kingdom", "germany", "china", "france", "south korea", "canada", "brazil", "australia"]

all_songs = pd.DataFrame()

for region in regions:
    df = pd.read_csv(f"{region}_top50_tracks.csv")
    df['Region'] = region.capitalize()  #添加地区列
    df['Rank'] = df.index + 1  #添加排名列，基于顺序生成
    all_songs = pd.concat([all_songs, df], ignore_index=True)

G = nx.Graph()

#添加国家节点
for region in regions:
    G.add_node(region.capitalize())

#找出在多个国家排行榜中出现的歌曲
duplicate_songs = all_songs.groupby('Track Name').filter(lambda x: len(x) > 1)

#添加边和边的权重
for song, group in duplicate_songs.groupby('Track Name'):
    regions_with_song = group['Region'].tolist()

    #遍历所有歌曲-国家对
    for i in range(len(regions_with_song)):
        for j in range(i + 1, len(regions_with_song)):
            region_pair = (regions_with_song[i], regions_with_song[j])
            if region_pair[0] != region_pair[1]:  #避免同一国家之间的自连接
                #如果原来已存在边，就在边的权重上加一；如果原来还没有边，就增加一条边
                if G.has_edge(*region_pair):
                    G[region_pair[0]][region_pair[1]]['weight'] += 1
                else:
                    G.add_edge(region_pair[0], region_pair[1], weight=1)

#画图
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=1)
#包含(edge, weight)键值对的迭代器，并拆解成两个元组
edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='thistle')
nx.draw_networkx_edges(G, pos, edgelist=edges, width=[w * 0.2 for w in weights], edge_color='grey')
nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold')

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color='navy')

plt.title('Network of Shared Songs in Different Countries', fontsize=16, fontweight='bold')

plt.savefig('result/network_of_shared_songs.jpg', format='jpg', dpi=300, bbox_inches='tight')
plt.show()



