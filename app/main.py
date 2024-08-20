# FastAPI 애플리케이션의 진입점 역할 + 각 엔드포인트 라우터를 애플리케이션에 연결하는 역할
import uvicorn
from fastapi import FastAPI
from app.routers import recommend, chatbot
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



# 실행
if __name__ == "__main__":
    uvicorn.run(app, port=8000)