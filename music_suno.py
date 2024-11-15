import json
import pathlib
import time
from venv import logger
import requests
from suno import Suno, ModelVersions

# api주소:https://pypi.org/project/SunoAI/
def download(url, title, path="./downloads"):
    try:
        response = requests.get(url, stream=True)
        print(response)
    except Exception as e:
        logger.error(f"Failed to download: {e}")
        return

    output_dir = pathlib.Path(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"{title}.mp4"

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # Filter out keep-alive chunks
                f.write(chunk)
    logger.info(f"Download complete: {filename}")

def check_credits(client: Suno):
    credit_check = client.get_credits()
    print(credit_check)

# SunoClient를 API 키로 초기화합니다.
api_key = "./secret/suno_cookie_api.json"

# api_key의 json 파일을 읽어 cookie 값을 가져옵니다
with open(api_key, "r") as f:
    data = json.load(f)
    cookie = data["cookie"]

client = Suno(
    cookie=cookie,
    model_version=ModelVersions.CHIRP_V3_5
)

# 사용자 지정 모델로 생성
song  =  client.generate ( 
#   prompt = "나에게 맞는 사랑을 찾았어 \n 자기야, 그냥 뛰어들어서 내 리드를 따라와 \n 글쎄, 나는 아름답고 달콤한 여자를 찾았어 \n 오, 당신이 나를 기다리고 있는 사람이라는 걸 전혀 몰랐어..." , 
    tags = "영국 팝" , 
    title = "england pop" , 
    make_instrumental =  False, 
    is_custom = True,
    wait_audio = True
)

# Quick usage 모드
# prompt = ""
# songs = client.generate(prompt=prompt, is_custom=False, wait_audio=True)
# song = songs[0]
# id = ""

print(song)

# 곡 찾기
# song = client.get_song("6d0976fb-7624-43a7-989a-6474106b54be")
# print(song)

# for key, val in song:
#     if key == "id":
#         id = val
#         print("id : ", id)
#     if key == "title":
#         title = val
#         print("title : ", title)
#     if key == "video_url":
#         path = val
#         print("path : ", path)

# time.sleep(15)
# download(path, title)


# credit = client.get_credits()
# print(credit)