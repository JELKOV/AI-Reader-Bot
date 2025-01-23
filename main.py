import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from PyPDF2 import PdfReader
import langid
import boto3
from dotenv import load_dotenv

# env 로드
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['AUDIO_FOLDER'] = './audio'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# POLLY 상수
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Polly 클라이언트 생성 - Seoul Regeon
polly_client = boto3.client(
    "polly",
    region_name="ap-northeast-2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


# TTS 함수
def text_to_listening(text, voice_id, output_file):
    # 파일 경로 설정
    output_file_path = os.path.join(app.config['AUDIO_FOLDER'], output_file)

    # TTS 요청
    response = polly_client.synthesize_speech(
        Text=text,
        VoiceId=voice_id,
        OutputFormat="mp3"
    )

    # 파일 저장
    with open(output_file_path, "wb") as audio_file:
        audio_file.write(response["AudioStream"].read())
    print(f"음성파일 : {output_file_path} 이 저장되었습니다.")
    return output_file


# PDF 텍스트 추출 함수
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    print(text)
    return text


# 언어 감지 및 음성 변환 처리 함수
def detect_language(text):
    if len(text) < 20:
        text = f" {text} "

    lang, confidence = langid.classify(text)
    print(f"감지된 언어: {lang} 신뢰도 {confidence}")

    if lang == "en":
        voice_id = "Matthew"
        output_file = "output_english.mp3"
    elif lang == "zh-cn":
        voice_id = "Zhiyu"
        output_file = "output_chinese.mp3"
    elif lang == "ko":
        voice_id = "Seoyeon"
        output_file = "output_korean.mp3"
    else:
        return None, "지원하지 않는 언어입니다."

    audio_file_name = text_to_listening(text, voice_id, output_file)
    return audio_file_name, None

# 음성 파일 다운로드 라우트
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename, as_attachment=True)

# 라우트: 홈 페이지
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # PDF 파일 업로드 처리
        if 'pdf_file' in request.files:
            pdf_file = request.files['pdf_file']
            if pdf_file.filename != '':
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
                pdf_file.save(pdf_path)
                text = extract_text_from_pdf(pdf_path)
                audio_file_name, error = detect_language(text)
                if error:
                    return jsonify({"error": error})
                return jsonify({
                    "message": "Audio file created",
                    "audio_file": audio_file_name,
                    "download_link": f"/download/{audio_file_name}"
                })

        # 텍스트 입력 처리
        elif 'text_input' in request.form:
            text = request.form['text_input']
            if len(text) > 3000:
                return jsonify({"error": "3000자 제한이 있습니다."})
            audio_file_name, error = detect_language(text)
            if error:
                return jsonify({"error": error})
            return jsonify({
                "message": "Audio file created",
                "audio_file": audio_file_name,
                "download_link": f"/download/{audio_file_name}"
            })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
