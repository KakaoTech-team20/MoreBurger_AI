import os
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt: str, model: str = "gpt-4", max_tokens: int = 150):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

def get_chatbot_response(message: str) -> str:
    try:
        # OpenAI의 ChatGPT 모델(assistant)을 사용하여 응답 생성
        response = openai.ChatCompletion.create(
            model="gpt-4", # 사용할 모델 지정
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        # API 응답에서 챗봇의 답변만 추출하여 반환
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        # 오류 발생 시 예외 처리
        return f"An error occurred: {str(e)}"