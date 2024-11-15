import json
import requests
import base64
import asyncio

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter

# Spotify 클라이언트 ID와 시크릿
CLENT_KEY_FILE = './secret/spotify_client_key.txt'

# JSON 파일 읽기
with open(CLENT_KEY_FILE, 'r') as file:
    data = json.load(file)

# API 키 추출
client_id = data.get('client_id')
client_secret = data.get('client_secret')

# API 기본 URL
base_url = "https://api.spotify.com/v1"

############### 국가별 장르 가져오기 ###############
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# 국가 코드와 국가 이름 매핑
countries = {
    'US': 'United States',
    'IN': 'India',
    'BR': 'Brazil',
    'ID': 'Indonesia',
    # 'KR': 'Korea',
    # 'JP': 'Japan',
    # 'MX': 'Mexico',
}

viral_50_playlists = {}

for country_code, country_name in countries.items():
    try:
        # Search API로 'Viral 50' 검색
        query = f"Viral 50 {country_name}"
        results = sp.search(q=query, type='playlist', limit=1)

        if results['playlists']['items']:
            playlist = results['playlists']['items'][0]  # 첫 번째 결과 가져오기
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            viral_50_playlists[country_code] = playlist_id
    except Exception as e:
        print(f"Error processing country {country_name}: {e}")

# 국가별 상위 3개 장르를 저장할 딕셔너리
country_top_genres = {}

for country, playlist_id in viral_50_playlists.items():
    try:
        # 플레이리스트의 트랙들 가져오기
        playlist_tracks = sp.playlist_items(playlist_id, limit=50)
        genres = []

        for item in playlist_tracks['items']:
            track = item['track']
            if track is None:  # 트랙이 없는 경우 스킵
                continue
            artist_id = track['artists'][0]['id']
            artist = sp.artist(artist_id)
            genres.extend(artist['genres'])

        # 장르 빈도수 계산
        genre_counts = Counter(genres)
        top_3_genres = genre_counts.most_common(3)
        country_top_genres[country] = top_3_genres

    except Exception as e:
        print(f"Error processing playlist for country {country}: {e}")

# 결과 출력
print(country_top_genres)
print(country_top_genres.items())
# for country, genres in country_top_genres.items():
    # print(f"\nCountry: {country}")
    # for genre, count in genres:
    #     print(f"Genre: {genre}, Count: {count}")