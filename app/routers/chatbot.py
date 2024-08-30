# 요청에 대한 응답 관련 코드
# FastAPI 라우터와 엔드포인트를 정의해 요청을 처리하고 응답하는 역할
import openai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.model.chatbot_model import get_chatbot_response
from app.rds_dataloader import get_all_burgers
from app.rds_dataloader.user import get_user_by_id

router = APIRouter()


# 사용자 메세지를 받기 위한 Pydantic 모델 정의
class ChatRequest(BaseModel):
    message: str


@router.post("/chatbot/{user_id}")
async def chat(user_id: int, request: ChatRequest):
    # 사용자 데이터 가져오기
    user = get_user_by_id(user_id)
    burger = get_all_burgers()

    # 맞춤형 데이터 구성
    user_info = (
        f"사용자 {user['nickname']}에 대한 정보입니다 : "
        f"맵기 선호도: {user['spicy']}, "
        f"먹는 양: {user['capacity']}"
    )

    try:
        full_prompt = f"{user_info}\n{request.message}"
        response = get_chatbot_response(full_prompt)

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
