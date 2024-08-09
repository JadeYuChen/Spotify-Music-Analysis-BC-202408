import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
   

regions = ["usa", "japan", "united kingdom", "germany", "china", "france", "south korea", "canada", "brazil", "australia"]


for region in regions:
    df = pd.read_csv(
        f"{region}_top50_tracks.csv", 
        index_col= "Track Name", 
        usecols=["Track Name", "Length (ms)", "Popularity", "Key", "Mode", "Danceability", 
                   "Acousticness", "Energy", "Instrumentalness", "Liveness", "Loudness", 
                   "Speechiness", "Tempo", "Time Signature", "Valence"]
                   )
    df_corr = df.corr()
    matrix = np.triu(np.ones_like(df_corr))
    plt.figure(figsize=(16, 8))
    sb.heatmap(df_corr, annot=True, fmt='.1f', cmap='bwr', vmin=-1, vmax=1, mask=matrix)
    plt.title(f'Correlation Heatmap for {region.capitalize()}', fontsize=16, weight='bold')
    plt.savefig(f"result/{region}_heatmap.png", dpi=300, bbox_inches='tight')

