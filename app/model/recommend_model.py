import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.rds_dataloader.order import get_user_orders


def recommend_burgers(user: pd.Series, burgers: pd.DataFrame) -> pd.DataFrame:
    user_orders = get_user_orders(user.id)


    if burgers.empty:
        return pd.DataFrame()

    if user_orders.empty:
        burgers['order_count'] = 0
        burgers_with_orders = burgers
    else:
        # 햄버거별 주문 횟수 계산
        burgers_with_orders = burgers.merge(user_orders, left_on='id', right_on='burgerId', how='left')
        burgers_with_orders['order_count'] = burgers_with_orders['order_count'].fillna(0)

    filtered_burgers = filter_burgers(user, burgers_with_orders).copy()

    if filtered_burgers.empty:
        return pd.DataFrame()

    # 사용자 선호도 특성 계산
    user_pref_features = filtered_burgers[['spicy', 'price', 'weight', 'order_count']].median().to_numpy().reshape(1,
                                                                                                                   -1)

    # 유사도 계산
    burger_features = filtered_burgers[['spicy', 'price', 'weight', 'order_count']].values
    similarities = cosine_similarity(burger_features, user_pref_features)
    filtered_burgers['Similarity'] = similarities.flatten()

    # 이전 주문 여부에 따른 우선순위 설정
    filtered_burgers['Priority'] = (filtered_burgers['order_count'] > 0).astype(int)

    # 정렬 및 상위 10개 추천
    recommended = filtered_burgers.sort_values(by=['Priority', 'Similarity'], ascending=[False, False]).head(10)

    return recommended[['id', 'name', 'price', 'calory', 'weight', 'spicy', 'order_count', 'Priority', 'Similarity']]


def filter_burgers(user: pd.Series, burgers: pd.DataFrame) -> pd.DataFrame:
    # 사용자 선호도에 따른 필터링 로직
    filtered = burgers.copy()

    # 매운맛 선호도에 따른 필터링
    spicy_preference = user.get('Spicy Preference', 'Medium')
    if spicy_preference == 'Mild':
        filtered = filtered[filtered['spicy'] <= 2]
    elif spicy_preference == 'Medium':
        filtered = filtered[filtered['spicy'] <= 4]

    # 섭취량에 따른 필터링
    consumption_size = user.get('Consumption Size', 'Medium')
    if consumption_size == 'Small':
        filtered = filtered[filtered['weight'] <= 200]
    elif consumption_size == 'Medium':
        filtered = filtered[filtered['weight'] <= 300]

    return filtered


def calculate_similarity(burgers: pd.DataFrame, user_pref: np.ndarray) -> np.ndarray:
    burger_features = burgers[['spicy', 'price', 'weight', 'order_count']].values
    return cosine_similarity(burger_features, user_pref).flatten()