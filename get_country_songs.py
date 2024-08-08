from dotenv import load_dotenv #加载环境变量文件
import os #用于与操作系统交互
import base64 #对数据进行Base64编码，用于生成Spotify API的认证信息
from requests import post, get
import json
import pandas as pd

# 加载获取环境变量
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# 获取access token，建立函数
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8") # 将上一步得到的字符串编码为字节，这样才能进行Base64编码
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") # 使用Base64对字节进行编码，并将结果转换为字符串

    url = "https://accounts.spotify.com/api/token" # 设置请求令牌的API端点URL
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    } # 将Base64编码后的字符串作为Basic认证的凭据，构造HTTP请求头
    data = {"grant_type": "client_credentials"} # 设置请求数据，指定授权类型
    result = post(url, headers=headers, data=data) # 向Spotify的令牌端点发送POST请求，获取访问令牌
    json_result = json.loads(result.content) # 将响应的JSON内容解析为Python字典
    token = json_result["access_token"] # 从JSON响应中提取访问令牌
    return token

# 获取授权头，用于后续的API请求
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# 请求搜索排行歌单
def search_for_playlist(token, playlist_name):
    url = "https://api.spotify.com/v1/search" # 参考文档Search for Item的endpoint
    headers = get_auth_header(token)
    query = f"?q={playlist_name}&type=playlist&limit=1" # 构建查询字符串，指定搜索类型为歌单并限制返回结果为1个

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["playlists"]["items"]
    # 检查是否找到了歌单
    if len(json_result) == 0:
        print("No playlist with this name exists...")
        return None
    return json_result[0] # 返回歌单的信息字典而不是包含单个元素的列表

# 获取歌单歌曲
def get_chart_songs(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks" # 获取歌曲
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

# 获取歌曲id列表
def get_track_ids(token, playlist_id):
    items = get_chart_songs(token, playlist_id)
    track_ids = []
    for item in items:
        track_ids.append(item["track"]["id"])
    return track_ids

# 获取单个歌曲信息
def get_track(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}" 
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

# 获取音乐音频特征
def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

# 获取多个地区的排行榜歌单信息并保存到CSV文件
def fetch_and_save_playlists(regions):
    token = get_token()

    #按各地区搜索歌单
    for region in regions:
        playlist_name = f"{region} top50"
        result = search_for_playlist(token, playlist_name)
        if result is None:
            continue

        print(f"Fetching data for playlist: {result['name']} ({region})")
        playlist_id = result["id"]
        track_ids = get_track_ids(token, playlist_id)

        #准备存储每个地区的歌曲信息
        tracks = []

        for track_id in track_ids:
            track_result = get_track(token, track_id)
            track_features = get_audio_features(token, track_id)

            track_name = track_result["name"]
            track_album = track_result["album"]["name"]
            track_artist = track_result["artists"][0]["name"]
            release_date = track_result["album"]["release_date"]
            popularity = track_result["popularity"]
            length = track_result['duration_ms']
            key = track_features["key"]
            mode = track_features['mode']
            danceability = track_features['danceability']
            acousticness = track_features['acousticness']
            energy = track_features['energy']
            instrumentalness = track_features['instrumentalness']
            liveness = track_features['liveness']
            loudness = track_features['loudness']
            speechiness = track_features['speechiness']
            tempo = track_features['tempo']
            time_signature = track_features['time_signature']
            valence = track_features['valence']

            track = [track_name, track_album, track_artist, release_date, length, popularity, key, mode, danceability, acousticness,
                     energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]
            tracks.append(track)

        #定义列名称
        columns = ["Track Name", "Album", "Artist", "Release Date", "Length (ms)", "Popularity", "Key", "Mode", "Danceability", 
                   "Acousticness", "Energy", "Instrumentalness", "Liveness", "Loudness", "Speechiness", "Tempo", 
                   "Time Signature", "Valence"]
        
        #创建DataFrame并保存为csv
        df = pd.DataFrame(tracks, columns=columns)
        df.to_csv(f'{region}_top50_tracks.csv', encoding='utf-8', index=False)
        print(f"Data for {region} saved to {region}_top50_tracks.csv")

#输入想查询的地区并完成获取
regions = ["usa", "japan", "united kingdom", "germany", "china", "france", "south korea", "canada", "brazil", "australia"]
fetch_and_save_playlists(regions)

