import os
import openai
from dotenv import load_dotenv

# 환경 변수 설정
# OPENAI_API_KEY=your_openai_api_key_here (.env 폴더에 ???)

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatbot_response(message: str) -> str:
    try:
        # OpenAI의 ChatGPT 모델(assistant)을 사용하여 응답 생성
        response = openai.Completion.create(
            model = "gpt-4", # 사용할 모델 지정
            message =[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        # API 응답에서 챗봇의 답변만 추출하여 반환
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        # 오류 발생 시 예외 처리
        return f"An error occurred: {str(e)}"