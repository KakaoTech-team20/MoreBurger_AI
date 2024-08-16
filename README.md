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
annotated-types
anyio
asgiref
Bottleneck
certifi
charset-normalizer
click
colorama
distro
exceptiongroup
fastapi
h11
httpcore
httpx
idna
image
intel-cmplr-lib-ur
intel-openmp
jiter
joblib
mkl
mkl-fft
mkl-random
mkl-service
numexpr
numpy
openai
pandas
pillow
pip
pydantic
pydantic-core
python-dateutil
pytz
rfc3986
scikit-learn
scipy
setuptools
six
sniffio
sqlparse
starlette
tbb
threadpoolctl
tqdm
typing_extensions
tzdata
uvicorn
vc
wheel
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
