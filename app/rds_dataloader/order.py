from .connection import db
import pandas as pd

def get_user_orders(user_id: int) -> pd.DataFrame:
    """
    사용자의 이전 주문 정보를 가져오는 함수
    :param user_id: 사용자 ID
    :return: 사용자의 주문 정보가 담긴 DataFrame
    """
    query = """
    SELECT burgerId, COUNT(*) as order_count
    FROM orders
    WHERE userId = %s
    GROUP BY burgerId
    """
    orders_data = db.execute_query(query, (user_id,))
    return pd.DataFrame(orders_data)