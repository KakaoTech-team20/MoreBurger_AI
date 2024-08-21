# 추천 시스템과 관련된 API 엔드포인트 정의
# FastAPI의 라우터를 사용하여 http 요청을 처리하고, 추천 결과를 반환하는 역할 수행
import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.model.recommend_model import recommend_burgers, load_and_preprocess_data, load_user_data

router = APIRouter()

# 사용자 입력 데이터를 위한 Pydantic 모델 정의
class UserPreferences(BaseModel):
    UserID: int
    Gender: str
    Age_Group: str
    Spicy_Preference: str
    Allergies: str
    Consumption_Size: str
    Previous_Orders: list

# 현재 파일의 디렉토리 경로 : 현재 파일 __file__
current_dir = os.path.dirname(__file__)

# 절대 경로 설정
burgers_path = os.path.abspath(os.path.join(current_dir, "../../data/burgers_data.csv"))
users_path = os.path.abspath(os.path.join(current_dir, "../../data/user_data.csv"))

# 데이터 로드
burgers = load_and_preprocess_data(burgers_path)
users = load_user_data(users_path)

# 추천 결과 반환 API 엔드포인트 정의
@router.post("/recommend")
async def recommend(user_preferences: UserPreferences):
    try:
        # 사용자의 데이터를 DataFrame 형식으로 변환
        user = pd.Series({
            'UserID': user_preferences.UserID,
            'Gender': user_preferences.Gender,
            'Age Group': user_preferences.Age_Group,
            'Spicy Preference': user_preferences.Spicy_Preference,
            'Allergies': user_preferences.Allergies,
            'Consumption Size': user_preferences.Consumption_Size,
            'Previous Orders': user_preferences.Previous_Orders
        })

        # 추천 알고리즘 실행
        recommended_burgers = recommend_burgers(user, burgers)

        if recommended_burgers.empty:
            return{"message": "적합한 햄버거를 찾을 수 없습니다."}

        # 추천 결과 반환
        return recommended_burgers.to_dict(orient='records')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''
왜 추천 시스템의 결과 반환 API는 POST 메서드인가?

- 사용자 입력 데이터를 기반으로 추천 생성하는데, 이 데이터는 주로 요청 본문에 포함되기 때문
- 입력 데이터를 바탕으로 여러 계산과 필터링 수행 -> 단순한 조회 작업(`GET`)보다 복잡한 연산 수행(`POST`)에 적합
- 민감한 사용자 데이터(ex. 알레르기 정보, 이전 주문 내역 등)를 URL에 노출하지 않고 안전하게 전송하기 위한 바람직한 방법
'''