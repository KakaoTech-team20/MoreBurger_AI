# FastAPI 애플리케이션의 진입점
# 라우터를 포함하고 서버를 실행 시킨다
import uvicorn
from fastapi import FastAPI
from app.routers import recommend, chatbot

# FastAPI 애플리케이션(app) 초기화
app = FastAPI()

# 추천 시스템, 챗봇 엔드포인트를 FastAPI 애플리케이션에 연결
app.include_router(recommend.router, prefix="/api")

# 챗봇 경로에 대한 라우터 등록
app.include_router(chatbot.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Burger Recommendation and Chatbot System"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# 실행
if __name__ == "__main__":
    uvicorn.run(app, port=8000) # host = '127.0.0.1'