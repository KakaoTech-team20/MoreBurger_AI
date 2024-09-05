import io
import os

from fastapi import APIRouter, HTTPException
import openai
from pydantic import BaseModel

from app.rds_dataloader import get_all_burgers
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

router = APIRouter()

# OpenAI 클라이언트 및 벡터 스토어 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 사용자 메세지를 받기 위한 Pydantic 모델 정의
class ChatRequest(BaseModel):
    user_id: int
    message: str


@router.post("/chatbot/")
async def chat(request: ChatRequest):
    try:
        # 사용자 데이터 가져오기
        user_id, message = request.user_id, request.message
        print(f"User ID: {user_id}")
        print(f"Message: {message}")

        burger_df = get_all_burgers()
        burger_df.to_csv("burger_data.txt", index=False)

        # RDS에서 받아온 버거 정보를 csv 형태로 변환 후, openai 에서 assistant가 thread에서 사용할 file 로 구성
        file = client.files.create(
            file=open("burger_data.txt", "rb"),
            purpose='assistants'
        )

        # 사용자 메세지를 포함하는 새로운 대화 스레드 생성
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "햄버거 추천해줘"
                        },
                    ],
                }
            ]
        )

        # 생성된 스레드와 assistant를 사용해 대화 진행 (어씨스턴트 호출)
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id='asst_JR7zBXnLYraebcyRmKXrKU1o',
            tools=[{"type": "file_search"}]
        )
        print(run)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    user_id, message = 1, "햄버거 추천해줘"

    # 벡터 스토어에서 기존 Assistant 불러오기
    vector_store = client.beta.vector_stores.retrieve("vs_wZWpgYaxPipa8tByxs2DSDNk")

    # 기존 assistant를 업데이트 하는 코드
    assistant = client.beta.assistants.retrieve("asst_JR7zBXnLYraebcyRmKXrKU1o")

    # 새로운 대화 스레드 생성
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "'무엇을 도와드릴까요?' 라고만 말해",
            }
        ]
    )

    # 메세지를 스레드에 추가
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # assistant와 대화 실행
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # 대화가 완료될 때까지 상태 확인
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(run.status)
        print(run.completed_at)

    # 대화가 완료되면 메세지를 불러옴
    message = client.beta.threads.messages.list(thread_id=thread.id)
    print("챗봇 : ", message.data[0].content[0].text.value)

    # 사용자와의 대화를 반복해서 수행
    while True:
        message = input("인간 : ")
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # 대화 완료까지 상태 확인
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(run.status)
            print(run.completed_at)

        # 대화 완료 후 챗봇 메시지를 출력
        message = client.beta.threads.messages.list(thread_id=thread.id)
        print(message.data[0].content[0].text.value)