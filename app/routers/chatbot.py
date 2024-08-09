from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.model.chatbot_model import get_chatbot_response

router = APIRouter()

# 사용자 메세지를 받기 위한 Pydantic 모델 정의
class ChatRequest(BaseModel):
    message: str

@router.post("/chatbot")
async def chatbot(chat_request: ChatRequest):
    try:
        # 클라이언트로부터 받은 메세지를 OpenAI API에 전달
        response = get_chatbot_response(chat_request.message)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
