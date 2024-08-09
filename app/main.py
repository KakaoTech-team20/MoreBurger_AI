import uvicorn
from fastapi import FastAPI
from .routers import chatbot, recommend
app = FastAPI()
app.include_router(chatbot.router)
app.include_router(recommend.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



# 실행
if __name__ == "__main__":
    uvicorn.run(app, port=8000)