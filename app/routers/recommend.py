from urllib.request import Request

from fastapi import APIRouter, HTTPException
from app.models.burger_model import load_and_preprocess_data, recommend_burgers
from app.models.user_model import load_user_data
import os

router = APIRouter()

burgers = load_and_preprocess_data('data/burgers_data.csv')
users = load_user_data('data/user_data.csv')

@router.get("/recommend/")
async def index():
    return {"result": "hello recommend!"}

@router.get('/recommend/{user_id}')
async def recommend(user_id: int):
    try:
        user = users[users['UserID'] == user_id].iloc[0]
        user_dict = user.to_dict()

        previous_orders = []
        for order_id in user_dict['Previous Orders']:
            burger = burgers[burgers['ID'] == order_id].iloc[0]
            previous_orders.append(f"{burger['Name']}({order_id})")
        user_dict['Previous Orders'] = previous_orders

        recommended_burgers = recommend_burgers(user, burgers)

        if recommended_burgers.empty:
            return {'user': user_dict, 'burgers': []}

        result = recommended_burgers[['ID', 'Name', 'Price', 'Similarity', 'Priority', 'spicy']].to_dict('records')
        for burger in result:
            image_path = f"data/burger_images/image_{burger['ID']}.png"
            if os.path.exists(image_path):
                burger['image'] = f"data/burger_images/image_{burger['ID']}.png"
            else:
                burger['image'] = "data/burger_images/default.webp"
            burger['order_count'] = user_dict['Previous Orders'].count(f"{burger['Name']}({burger['ID']})")

        result = sorted(result, key=lambda x: (-x['Priority'], -x['Similarity']))
        for i, burger in enumerate(result, 1):
            burger['rank'] = i

        return {'user': user_dict, 'burgers': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))