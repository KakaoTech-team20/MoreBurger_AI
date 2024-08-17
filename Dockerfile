# Python 3.10-slim 이미지를 기반으로 시작
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 로컬의 프로젝트 파일을 도커 이미지로 복사
COPY . .

# Python 패키지를 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 포트를 외부에 노출
EXPOSE 8000

# Uvicorn 서버를 시작
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
