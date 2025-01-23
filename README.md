# AI 오디오 제작 시스템

## 개요
이 프로젝트는 PDF 파일 또는 입력 텍스트를 오디오 파일로 변환하는 AI 기반 텍스트-음성 변환(TTS) 시스템입니다. Amazon Polly를 활용하여 음성을 생성하며, Flask 웹 프레임워크와 언어 감지, PDF 텍스트 추출 라이브러리를 사용합니다.

## 주요 기능
- **PDF를 오디오로 변환**: PDF 파일을 업로드하면 텍스트를 추출하여 오디오 파일로 변환합니다.
- **텍스트를 오디오로 변환**: 텍스트를 입력하여 오디오 파일을 생성합니다.
- **언어 감지**: 한국어, 영어, 중국어를 지원하며, 입력 언어를 자동으로 감지합니다.
- **오디오 파일 다운로드**: 생성된 오디오 파일을 다운로드 링크를 통해 제공.

## 사용 기술
- **백엔드**: Flask (Python)
- **TTS 서비스**: Amazon Polly
- **언어 감지**: `langid`
- **PDF 텍스트 추출**: `PyPDF2`

## 폴더 구조
```
project/
├── app.py              # Flask 메인 파일
├── requirements.txt    # 필수 라이브러리
├── templates/          # HTML 템플릿
│   └── index.html      # 메인 UI 템플릿
├── static/
│   ├── css/
│   │   └── styles.css  # CSS 파일
├── uploads/            # 업로드된 PDF 파일
├── audio/              # 생성된 오디오 파일
└── .env                # AWS 자격 증명
```

## 설치 방법
### 사전 준비
- Python 3.x가 설치되어 있어야 합니다.
- Amazon Polly 서비스가 활성화된 AWS 계정.

### 설치 단계
1. 저장소 클론:
   ```bash
   git clone https://github.com/JELKOV/AI-Reader-Bot.git
   ```

2. 가상 환경 설정 (선택 사항):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate    # Windows
   ```

3. 라이브러리 설치:
   ```bash
   pip install -r requirements.txt
   ```

4. AWS 자격 증명 설정:
   - 루트 디렉토리에 `.env` 파일 생성:
     ```
     AWS_ACCESS_KEY_ID=your_access_key
     AWS_SECRET_ACCESS_KEY=your_secret_key
     ```

5. 애플리케이션 실행:
   ```bash
   python app.py
   ```

6. 브라우저에서 `http://127.0.0.1:5000`에 접속.

## 사용 방법
1. **PDF를 오디오로 변환**:
   - 한국어, 영어, 중국어 텍스트가 포함된 PDF 파일을 업로드하세요.
   - 시스템이 텍스트를 추출하고 오디오 파일을 생성합니다.

2. **텍스트를 오디오로 변환**:
   - 텍스트 입력 필드에 최대 3000자까지 입력하세요.
   - 시스템이 언어를 감지하여 오디오 파일을 생성합니다.

3. **오디오 다운로드**:
   - 처리 완료 후 생성된 오디오 파일의 다운로드 링크가 화면에 표시됩니다.

## 문제 해결
- **Amazon Polly TextLengthExceededException**:
  - Polly의 Neural TTS는 최대 3000자까지 처리할 수 있습니다. 시스템은 자동으로 텍스트를 나눠 처리합니다.
- **언어 감지 문제**:
  - 영어는 최소 10자 이상의 텍스트를 입력해야 언어 감지가 정확합니다.

## 향후 개선사항
- 오디오 파일을 Amazon S3에 저장하여 확장성 향상.
- 사용자 인증 기능 추가로 개인화된 파일 관리 제공.


## 문의
질문이나 피드백은 아래로 연락 주세요:
- **이메일**: ajh4234@gmail.com
- **GitHub**: [JELKOV](https://github.com/JELKOV)