import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


def load_and_preprocess_data(file_path):
    """
    현재는 file_path에 존재하는 csv 파일에서 burger의 데이터를 읽어오지만 앞으로 DB의 접속하는 형태를 변경 예정
    :param file_path: 
    :return: 
    """
    burgers = pd.read_csv(file_path)
    burgers['Ingredients'] = burgers['Ingredients'].str.strip().str.replace(" ", ", ")
    burgers = burgers.reset_index(drop=True)
    burgers.index += 1
    burgers['ID'] = burgers.index

    if burgers['Order Frequency'].isnull().any():
        missing_count = burgers['Order Frequency'].isnull().sum()
        burgers.loc[burgers['Order Frequency'].isnull(), 'Order Frequency'] = np.random.randint(50, 200,
                                                                                                size=missing_count)

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

    return burgers


def filter_burgers(user: pd.Series, burgers: pd.DataFrame):
    user_allergies = set(user['Allergies'].split(', '))
    consumption_size = user['Consumption Size']

    condition = burgers['Ingredients'].apply(lambda x: not user_allergies.intersection(x.split(', ')))
    filtered_burgers = burgers[condition]

    if consumption_size == 'Large':
        filtered_burgers = filtered_burgers[filtered_burgers['Total Weight'] > 250]
    elif consumption_size == 'Small':
        filtered_burgers = filtered_burgers[filtered_burgers['Total Weight'] < 200]
    else:
        filtered_burgers = filtered_burgers[filtered_burgers['Total Weight'].between(200, 250)]

    return filtered_burgers


def calculate_similarity(filtered_burgers, user_pref_features):
    features = ['spicy', 'Price', 'Total Weight', 'Order Frequency']
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(filtered_burgers[features])
    user_features = scaler.transform(pd.DataFrame(user_pref_features, columns=features))

    return cosine_similarity(scaled_features, user_features).flatten()


def recommend_burgers(user: pd.Series, burgers: pd.DataFrame) -> pd.DataFrame:
    filtered_burgers = filter_burgers(user, burgers).copy()

    if filtered_burgers.empty:
        return pd.DataFrame()

    user_pref_features = filtered_burgers[
        ['spicy', 'Price', 'Total Weight', 'Order Frequency']].median().values.reshape(1, -1)
    filtered_burgers.loc[:, 'Similarity'] = calculate_similarity(filtered_burgers, user_pref_features)

    filtered_burgers.loc[:, 'Priority'] = filtered_burgers['ID'].isin(user['Previous Orders']).astype(int)

    recommended = filtered_burgers.sort_values(by=['Priority', 'Similarity'], ascending=[False, False]).head(10)

    return recommended[
        ['ID', 'Name', 'Price', 'Calories', 'Total Weight', 'spicy', 'Order Frequency', 'Priority', 'Similarity']]