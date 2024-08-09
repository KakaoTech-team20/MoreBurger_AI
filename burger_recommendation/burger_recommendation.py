import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# 필요한 라이브러리들을 임포트합니다.
# random: 난수 생성에 사용
# pandas: 데이터 처리 및 분석을 위한 라이브러리
# numpy: 수치 계산을 위한 라이브러리
# matplotlib.pyplot: 데이터 시각화를 위한 기본 라이브러리
# seaborn: 통계적 그래프 작성을 위한 라이브러리
# sklearn.metrics.pairwise의 cosine_similarity: 코사인 유사도 계산에 사용
# sklearn.preprocessing의 MinMaxScaler: 특성 스케일링에 사용

plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# matplotlib의 글로벌 설정을 변경합니다.
# 'Malgun Gothic' 폰트를 사용하여 한글이 올바르게 표시되도록 합니다.
# 마이너스 기호가 유니코드로 인해 깨지는 것을 방지합니다.

def load_and_preprocess_data(file_path):
    burgers = pd.read_csv(file_path)
    # CSV 파일에서 햄버거 데이터를 읽어 pandas DataFrame으로 로드합니다.

    burgers['Ingredients'] = burgers['Ingredients'].str.strip().str.replace(" ", ", ")
    # 'Ingredients' 열의 각 항목에 대해:
    # 1. str.strip()으로 앞뒤 공백을 제거합니다.
    # 2. str.replace(" ", ", ")로 공백을 쉼표와 공백으로 대체합니다.
    # 이는 재료 목록을 일관된 형식으로 만들기 위함입니다.

    burgers = burgers.reset_index(drop=True)
    burgers.index += 1
    burgers['ID'] = burgers.index
    # DataFrame의 인덱스를 재설정하고, 1부터 시작하도록 합니다.
    # 그리고 이 인덱스를 'ID' 열로 추가합니다.

    if burgers['Order Frequency'].isnull().any():
        missing_count = burgers['Order Frequency'].isnull().sum()
        burgers.loc[burgers['Order Frequency'].isnull(), 'Order Frequency'] = np.random.randint(50, 200,
                                                                                                size=missing_count)

    # 'Order Frequency' 열에 결측치가 있는지 확인합니다.
    # 결측치가 있다면:
    # 1. 결측치의 개수를 계산합니다.
    # 2. np.random.randint를 사용하여 50에서 200 사이의 랜덤한 정수를 생성하여 결측치를 채웁니다.

    burgers = burgers.astype({
        'ID': 'int32',
        'Name': 'string',
        'Price': 'float32',
        'Calories': 'int32',
        'Total Weight': 'float32',
        'Order Frequency': 'int32',
        'Ingredients': 'string',
        'spicy': 'int32'
    })
    # 각 열의 데이터 타입을 명시적으로 지정합니다.
    # 이는 메모리 사용을 최적화하고 연산 속도를 향상시키기 위함입니다.

    visualize_data(burgers, "햄버거 데이터")
    # 전처리된 햄버거 데이터를 시각화합니다.

    return burgers
    # 전처리된 햄버거 데이터를 반환합니다.


def load_user_data(file_path):
    users = pd.read_csv(file_path)
    # CSV 파일에서 사용자 데이터를 읽어 pandas DataFrame으로 로드합니다.

    users['Previous Orders'] = users['Previous Orders'].apply(eval)
    # 'Previous Orders' 열의 각 항목에 eval 함수를 적용합니다.
    # 이는 문자열로 저장된 리스트를 실제 Python 리스트로 변환하기 위함입니다.

    users = users.astype({
        'UserID': 'int32',
        'Gender': 'category',
        'Age Group': 'category',
        'Spicy Preference': 'category',
        'Allergies': 'string',
        'Consumption Size': 'category'
    })
    # 각 열의 데이터 타입을 명시적으로 지정합니다.
    # 'category' 타입은 범주형 데이터를 위한 것으로, 메모리 사용을 줄이고 처리 속도를 높입니다.

    visualize_data(users, "사용자 데이터")
    # 전처리된 사용자 데이터를 시각화합니다.

    return users
    # 전처리된 사용자 데이터를 반환합니다.


def visualize_data(data, title, user=None, filter_type=None):
    return 0
    # 이 함수는 현재 구현되어 있지 않고 0을 반환하도록 되어 있습니다.
    # 실제 구현 시에는 데이터를 시각화하는 코드가 여기에 들어갈 것입니다.


def filter_burgers(user: pd.Series, burgers: pd.DataFrame):
    user_allergies = set(user['Allergies'].split(', '))
    spicy_pref = user['Spicy Preference']
    consumption_size = user['Consumption Size']
    # 사용자의 알레르기 정보를 집합으로 변환하고, 매운맛 선호도와 섭취량 선호도를 변수에 저장합니다.

    # 알레르기 필터링
    visualize_data(burgers, "알레르기 필터링 전 햄버거 데이터", user, 'allergy')
    condition = burgers['Ingredients'].apply(lambda x: not user_allergies.intersection(x.split(', ')))
    filtered_burgers = burgers[condition]

    visualize_data(filtered_burgers, "알레르기 필터링 후 햄버거 데이터", user, 'allergy')
    # 1. 필터링 전 데이터를 시각화합니다.
    # 2. 각 햄버거의 재료와 사용자의 알레르기 항목이 겹치지 않는지 확인합니다.
    # 3. 조건을 만족하는 햄버거만 필터링합니다.
    # 4. 필터링 후 데이터를 시각화합니다.

    # 매운맛 선호도 필터링
    visualize_data(filtered_burgers, "매운맛 선호도 필터링 전 햄버거 데이터", user, 'spicy')
    # if spicy_pref == 'Yes':
    #     filtered_burgers = filtered_burgers[filtered_burgers['spicy'] == 1]
    # 버거의 spicy 값인 버거만 남김
    # 매운 맛 선호자는 안매운 햄버거는 선호에서 제외됨
    # 살짝보류~

    # elif spicy_pref == 'No':
    #     filtered_burgers = filtered_burgers[~filtered_burgers['spicy'] == 0]

    visualize_data(filtered_burgers, "매운맛 선호도 필터링 후 햄버거 데이터", user, 'spicy')
    # 1. 필터링 전 데이터를 시각화합니다.
    # 2. 사용자의 매운맛 선호도에 따라 햄버거를 필터링합니다.
    # 3. 필터링 후 데이터를 시각화합니다.

    # 섭취량 선호도 필터링
    visualize_data(filtered_burgers, "섭취량 선호도 필터링 전 햄버거 데이터", user, 'size')
    if consumption_size == 'Large':
        filtered_burgers = filtered_burgers[filtered_burgers['Total Weight'] > 250]
    elif consumption_size == 'Small':
        filtered_burgers = filtered_burgers[filtered_burgers['Total Weight'] < 200]
    else:
        filtered_burgers = filtered_burgers[filtered_burgers['Total Weight'].between(200, 250)]
    visualize_data(filtered_burgers, "섭취량 선호도 필터링 후 햄버거 데이터", user, 'size')
    # 1. 필터링 전 데이터를 시각화합니다.
    # 2. 사용자의 섭취량 선호도에 따라 햄버거를 필터링합니다.
    # 3. 필터링 후 데이터를 시각화합니다.

    return filtered_burgers
    # 모든 필터링 과정을 거친 햄버거 데이터를 반환합니다.


def calculate_similarity(filtered_burgers, user_pref_features):
    features = ['spicy', 'Price', 'Total Weight', 'Order Frequency']
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(filtered_burgers[features])
    user_features = scaler.transform(pd.DataFrame(user_pref_features, columns=features))
    # 1. 유사도 계산에 사용할 특성들을 정의합니다.
    # 2. MinMaxScaler를 사용하여 특성들을 0과 1 사이의 값으로 정규화합니다.
    # 3. 햄버거 특성과 사용자 선호도 특성을 동일한 스케일로 변환합니다.

    return cosine_similarity(scaled_features, user_features).flatten()
    # 코사인 유사도를 계산하여 반환합니다.
    # flatten()을 사용하여 2D 배열을 1D 배열로 변환합니다.


def recommend_burgers(user: pd.Series, burgers: pd.DataFrame) -> pd.DataFrame:
    filtered_burgers = filter_burgers(user, burgers).copy()
    # 사용자 정보에 기반하여 햄버거를 필터링합니다.

    if filtered_burgers.empty:
        return pd.DataFrame()
    # 필터링 결과가 비어있다면 빈 DataFrame을 반환합니다.

    user_pref_features = filtered_burgers[
        ['spicy', 'Price', 'Total Weight', 'Order Frequency']].median().values.reshape(1, -1)
    # 필터링된 햄버거들의 중앙값을 사용자 선호도 특성으로 사용합니다.
    filtered_burgers.loc[:, 'Similarity'] = calculate_similarity(filtered_burgers, user_pref_features)
    # 각 햄버거와 사용자 선호도 간의 유사도를 계산합니다.

    filtered_burgers.loc[:, 'Priority'] = filtered_burgers['ID'].isin(user['Previous Orders']).astype(int)
    # 사용자가 이전에 주문한 햄버거에 우선순위를 부여합니다.

    recommended = filtered_burgers.sort_values(by=['Priority', 'Similarity'], ascending=[False, False]).head(10)
    # 우선순위와 유사도를 기준으로 정렬하고 상위 15개를 선택합니다.

    return recommended[
        ['ID', 'Name', 'Price', 'Calories', 'Total Weight', 'spicy', 'Order Frequency', 'Priority', 'Similarity']]
    # 추천된 햄버거 정보를 반환합니다.


def main():
    burgers = load_and_preprocess_data(r"burger_recommendation/data/burgers_data.csv")
    users = load_user_data(r'burger_recommendation/data/user_data.csv')
    # 햄버거와 사용자 데이터를 로드하고 전처리합니다.

    user_index = np.random.randint(0, len(users))
    user = users.iloc[user_index]
    print(f"사용자 {user['UserID']} 정보:\n", user)
    # 랜덤하게 한 명의 사용자를 선택하고 정보를 출력합니다.

    recommended_burgers = recommend_burgers(user, burgers)
    # 선택된 사용자에 대한 햄버거 추천을 수행합니다.

    if not recommended_burgers.empty:
        print(f"\n사용자 {user['UserID']}를 위한 추천 햄버거:")
        print(recommended_burgers[['Name', 'Price', 'Calories', 'Total Weight', 'Order Frequency', 'Priority']])
    else:
        print("알레르기, 선호도 또는 섭취량으로 인해 적합한 햄버거를 찾을 수 없습니다.")
    # 추천 결과를 출력합니다. 추천된 햄버거가 없는 경우 적절한 메시지를 출력합니다.


if __name__ == "__main__":
    main()
    # 스크립트가 직접 실행될 때 main 함수를 호출합니다.
