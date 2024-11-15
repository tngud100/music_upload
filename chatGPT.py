import json
import random
import openai

# GPT-3.5-turbo API 설정
# API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY_FILE = './secret/chatGPT_api_key.txt'

# JSON 파일 읽기
with open(API_KEY_FILE, 'r') as file:
    data = json.load(file)

# API 키 추출
api_key = data.get('api_key')

API_KEY = api_key

# HEADERS = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {API_KEY}"
# }

# GPT_MODEL = "gpt-3.5-turbo"

client = openai.OpenAI(api_key=API_KEY)  # 'YOUR_API_KEY'를 실제 API 키로 교체하세요.

# 사용자 입력 메시지
user_content = (
    "사람들이 관심을 가지게 할 만한 강렬하고 자극적인 노래 제목을 30개 이상 추천해줘. "
    "제목마다 각기 다른 주제를 다루도록 하고, 주제와 감정이 제목에 잘 반영되도록 해줘."
)
messages = [{"role": "user", "content": user_content}]

# ChatCompletion 생성
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7
)

# 생성된 노래 제목 목록 추출
generated_titles = response.choices[0].message.content

# 제목을 줄바꿈으로 분리하여 리스트로 변환
title_list = [title.strip() for title in generated_titles.split('\n') if title.strip()]

# 제목 중 하나를 랜덤 선택하여 출력
selected_title = random.choice(title_list)
num = selected_title.split(" ")[0]
selected_title = selected_title.replace(num, '')
selected_title = selected_title.strip()
print("선택된 노래 제목: " + selected_title)



# 실시간 나라와 장르를 추출(getSongGenre.py), => 노래 제목을 생성(gpt) => 각 노래의 장르, 나라, 노래 제목을 고려하여 가사를 생(gpt)
#    => 해당 노래 가사에 알맞고, 해당 국가의 사람들의 관심을 이끌만한 태그 생성(gpt) => 노래생성 및 다운로드(muisc_suno.py) => youtube 업로드(youtube.py)