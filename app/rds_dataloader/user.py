import pandas as pd
from .connection import db


def get_user_by_id(user_id: int) -> pd.DataFrame:
    """
    입력받은 user_id를 이용해 RDS database에 존재하는 user의 행을 얻어오는 함수
    :param user_id: 
    :return: 유저 정보 또는 None (해당 ID의 유저가 없는 경우)
    """
    return pd.DataFrame(db.execute_single_query("SELECT * FROM users WHERE id = %s", (user_id,)))
