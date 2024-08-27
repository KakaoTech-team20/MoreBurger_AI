import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.model.recommend_model import recommend_burgers
from app.rds_dataloader import get_user_by_id, get_all_burgers  # 사용자 정보를 가져오는 함수 import

router = APIRouter()


class UserPreferences(BaseModel):
    id: int
    email: str
    nickname: str
    sex: str
    age: int
    role: str
    spicy: int
    capacity: str
    createdAt: datetime


@router.post("/recommend/")
async def recommend(user_id: int):
    try:
        # 데이터베이스에서 사용자 정보 가져오기
        user = get_user_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # 햄버거 데이터 가져오기
        burgers = get_all_burgers()

        # 추천 알고리즘 실행
        recommended_burgers = recommend_burgers(user, burgers)

        if recommended_burgers.empty:
            return {"message": "적합한 햄버거를 찾을 수 없습니다."}

        # 추천 결과 반환
        return recommended_burgers.to_dict(orient='records')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_age_group(age: int) -> str:
    if age < 20:
        return "10s"
    elif age < 30:
        return "20s"
    elif age < 40:
        return "30s"
    elif age < 50:
        return "40s"
    else:
        return "50+"


def get_spicy_preference(spicy: int) -> str:
    if spicy <= 1:
        return "Mild"
    elif spicy <= 3:
        return "Medium"
    else:
        return "Spicy"