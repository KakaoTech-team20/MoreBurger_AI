import pandas as pd
from .connection import db


def get_user_by_id(user_id: int) -> pd.Series:
    """
    입력받은 user_id를 이용해 RDS database에 존재하는 user의 정보를 Series로 반환하는 함수
    :param user_id: 조회할 사용자의 ID
    :return: 사용자 정보가 담긴 Series 또는 None (해당 ID의 사용자가 없는 경우)
    """
    result = db.execute_single_query("SELECT * FROM users WHERE id = %s", (user_id,))
    return pd.Series(result) if result else None