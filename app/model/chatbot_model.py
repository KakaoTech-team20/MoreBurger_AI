# 응답에 필요한 기능들 정의해서 routers에서 사용할 수 있도록 구현하는 파일
# OpenAI API 호출과 관련된 기능을 정의하여 라우터에서 사용할 수 있도록 하는 역할
import os

# import openai
from openai import OpenAI

from dotenv import load_dotenv

# # 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chatbot_response(message: str) -> str:
    try:
        # OpenAI의 ChatGPT 모델(assistant)을 사용하여 응답 생성
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            model="gpt-4o"  # 사용할 모델 지정
        )
        # API 응답에서 챗봇의 답변만 추출하여 반환
        return response.choices[0].message.content.strip()

    except Exception as e:
        # 오류 발생 시 예외 처리
        return f"An error occurred: {str(e)}"