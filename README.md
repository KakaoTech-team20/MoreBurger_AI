# MoreBurger AI Recommendation System

이 프로젝트는 FastAPI를 사용하여 구현된 햄버거 추천 시스템입니다.

## 요구 사항

- Python 3.10.x
- Git

## 프로젝트 설치

1. 프로젝트를 로컬 시스템에 클론합니다:
   ```
   git clone https://github.com/KakaoTech-team20/MoreBurger_AI.git
   cd MoreBurger_AI
   ```

2. Python 3.10.x를 설치합니다:
   - Windows: [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드
   - Linux:
     ```
     sudo apt update
     sudo apt install python3.10
     ```
3. (Linux 사용자만 해당) venv 모듈을 설치합니다:
   ```
   sudo apt install python3.10-venv
   ```
5. 가상 환경을 생성하고 활성화합니다:
   - Windows:
     ```
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Linux:
     ```
     python3.10 -m venv venv
     source venv/bin/activate
     ```

6. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

## 종속성

```
annotated-types==0.7.0
anyio==4.4.0
asgiref==3.8.1
certifi==2024.7.4
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
distro==1.9.0
Django==5.1
exceptiongroup==1.2.2
fastapi==0.112.1
h11==0.14.0
httpcore==1.0.5
httpx==0.14.0b0
idna==3.7
image==1.5.33
jiter==0.5.0
openai==1.40.8
pillow==10.4.0
pydantic==2.8.2
pydantic_core==2.22.0
rfc3986==2.0.0
six==1.16.0
sniffio==1.3.1
sqlparse==0.5.1
starlette==0.38.2
tqdm==4.66.5
typing_extensions==4.12.2
tzdata==2024.1
uvicorn==0.30.6
```

## 실행 방법

1. 가상 환경이 활성화되어 있는지 확인합니다.

2. 다음 명령어로 서버를 실행합니다:
   ```
   uvicorn app.main:app --reload
   ```

3. 브라우저에서 `http://localhost:8000`으로 접속하여 API 문서를 확인할 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
