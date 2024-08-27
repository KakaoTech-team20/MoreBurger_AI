import pandas as pd
from .connection import db


def get_all_burgers() -> pd.DataFrame:
    """
    RDS 데이터베이스에 존재하는 모든 햄버거의 정보를 DataFrame으로 반환하는 함수
    :return: 모든 햄버거 정보가 담긴 DataFrame
    """
    return pd.DataFrame(db.execute_query("SELECT * FROM burgers"))


def get_burger_by_id(burger_id: int) -> pd.DataFrame:
    """
    RDS 데이터베이스에 존재하는 특정 burger_id를 가진 햄버거의 정보를 반환하는 함수
    :param burger_id: 조회할 햄버거의 ID
    :return: ID에 해당하는 햄버거 정보가 담긴 DataFrame
    """
    return pd.DataFrame(db.execute_single_query("SELECT * FROM burgers WHERE id = %s", (burger_id,)))


def get_burgers_by_category(category: str) -> pd.DataFrame:
    """
    특정 카테고리에 속하는 모든 햄버거의 정보를 반환하는 함수
    :param category: 조회할 햄버거의 카테고리
    :return: 해당 카테고리의 모든 햄버거 정보 DataFrame
    """
    return pd.DataFrame(db.execute_query("SELECT * FROM burgers WHERE category = %s", (category,)))


def search_burgers(keyword: str) -> pd.DataFrame:
    """
    이름이나 설명에 특정 키워드를 포함하는 모든 햄버거의 정보를 반환하는 함수
    :param keyword: 검색할 키워드
    :return: 검색 결과에 해당하는 모든 햄버거 정보 DataFrame
    """
    return pd.DataFrame(db.execute_query(
        "SELECT * FROM burgers WHERE name LIKE %s OR description LIKE %s",
        (f"%{keyword}%", f"%{keyword}%"))
    )
