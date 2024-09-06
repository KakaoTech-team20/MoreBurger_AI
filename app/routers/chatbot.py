import io
import os

from fastapi import APIRouter, HTTPException
import openai
from pydantic import BaseModel

from app.model.chatbot_model import retrieve_assistant, create_conversation_with_assistant, \
    start_conversation_with_assistant
from app.rds_dataloader import get_all_burgers
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

router = APIRouter()

# OpenAI 클라이언트 및 벡터 스토어 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 사용자 메세지를 받기 위한 Pydantic 모델 정의
class ChatRequest(BaseModel):
    user_email: str
    message: str
    thread_id: str
    assistant_id: str

# 창이 열리면 불리는 api, 대화 시작 메세지 주면서 스레드 시작 (스레드 id도 전달하기)
@router.get("/start/")
async def startchat():
    try:
        vector_store, assistant = retrieve_assistant()
        assistant_reply, thread_id = start_conversation_with_assistant(assistant)
        # 이 부분은 항상 assistant_reply가 "무엇을 도와들리까요?"이다 -> 이렇게 하는 이유는, 스레드 id로 이어지는 대화를 가능하게 하기 위해
        print("Thread id & Assistant id: ", thread_id, assistant.id)
        return assistant_reply, thread_id, assistant.id

    except Exception as e:
        print(f"Error starting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chatbot/")
async def chat(request: ChatRequest):
    try:
        # 사용자 데이터 가져오기
        thread_id, assistant_id = request.thread_id, request.assistant_id
        user_email, message = request.user_email, request.message
        # print(f"User Email: {user_email}")
        # print(f"Message: {message}")
        # print(f"Thread ID: {thread_id}")

        burger_df = get_all_burgers()
        burger_df.to_csv("burger_data.txt", index=False)

        assistant_reply, thread_id = create_conversation_with_assistant(message, thread_id, assistant_id)

        return {"assistant_reply": assistant_reply, "thread_id": thread_id}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

#
# if __name__ == "__main__":
#     user_id, message = 1, "햄버거 추천해줘"
