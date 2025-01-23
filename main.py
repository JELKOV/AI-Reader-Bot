import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Polly 클라이언트 생성 - Seoul Regeon
polly_client = boto3.client(
    "polly",
    region_name="ap-northeast-2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# TTS 요청
response = polly_client.synthesize_speech(
    Text="안녕하세요, 안제호 입니다 !! 다들 얼른 화이팅 하시고 설 연휴 잘 보내시길 바라겠습니다.",
    VoiceId="Seoyeon",
    OutputFormat="mp3"
)

# 파일 저장
with open("output.mp3", "wb") as audio_file:
    audio_file.write(response["AudioStream"].read())

print("Audio file saved as output.mp3")