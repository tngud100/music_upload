import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OAuth 2.0 클라이언트 ID 파일 경로
CLIENT_SECRETS_FILE = './secret/google_auth_client_secret.json'

# 접근 권한 범위
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    creds = None
    # Check if token already exists
    if os.path.exists('./secret/token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("Token loaded from token.json")
    
    # If no credentials, or if invalid or expired, initiate authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("Token refreshed")
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None
        if not creds:
            try:
                # Run OAuth flow to get credentials
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=8080)  # Changed to use the default port and method
                print("OAuth flow completed successfully")
            except Exception as e:
                print(f"OAuth error: {e}")
                return None

        # Save credentials for the next run
        if creds:
            with open('secret/token.json', 'w') as token:
                token.write(creds.to_json())
            print("Token saved to token.json")

    # Build the YouTube API service client
    try:
        youtube = build('youtube', 'v3', credentials=creds)
        print("YouTube API client created successfully")
        return youtube
    except Exception as e:
        print(f"Error creating YouTube API client: {e}")
        return None

def upload_video(youtube, file, title, description, tags, category_id, privacy_status):
    if youtube is None:
        print("YouTube client is not authenticated, aborting upload.")
        return

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }
    media = MediaFileUpload(file, chunksize=-1, resumable=True)
    
    try:
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'업로드 진행률: {int(status.progress() * 100)}%')
        print('업로드 완료!')
        return response
    except Exception as e:
        print(f"Error during video upload: {e}")
        return None

if __name__ == '__main__':
    youtube = get_authenticated_service()
    if youtube:
        file = './downloads/점심을 닭계장으로 먹어버렸네.mp4'  # 업로드할 동영상 파일 경로
        title = '지리는 닭계장'  # 동영상 제목
        description = '닭계장 맞있음'
        tags = ['닭계장', '노래', '음악', '펑키', '박자 쪼개기', '리듬', '신남']  # 태그 리스트
        category_id = '10'  # 카테고리 ID (예: 22는 'People & Blogs', 10은 'Music')
        privacy_status = 'public'  # 공개 상태 ('public', 'private', 'unlisted')
        upload_video(youtube, file, title, description, tags, category_id, privacy_status)
    else:
        print("Failed to authenticate with YouTube.")
