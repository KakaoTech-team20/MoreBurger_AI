# FastAPI 애플리케이션의 진입점 역할 + 각 엔드포인트 라우터를 애플리케이션에 연결하는 역할
import uvicorn
from fastapi import FastAPI, HTTPException
from app.routers import recommend, chatbot
from pydantic import BaseModel
from app.model.chatbot_model import generate_response
app = FastAPI()

# 추천 시스템, 챗봇 엔드포인트를 FastAPI 애플리케이션에 연결
app.include_router(recommend.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Burger Recommendation and Chatbot System"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

class ChatRequest(BaseModel):
    message: str

@app.post("/chatbot/")
async def chat(request: ChatRequest):
    try:
        response = generate_response(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# 실행
if __name__ == "__main__":
    uvicorn.run(app, port=8000)