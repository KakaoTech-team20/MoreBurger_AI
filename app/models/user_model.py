import pandas as pd


def load_user_data(file_path):
    """
    local에 존재하는 file_path의 csv를 읽어오는 코드
    앞으로 DB화 시켜 DB의 내용을 읽어오도록 할 것 이다.
    :param file_path:
    :return:
    """
    users = pd.read_csv(file_path)
    users['Previous Orders'] = users['Previous Orders'].apply(eval)

    users = users.astype({
        'UserID': 'int32',
        'Gender': 'category',
        'Age Group': 'category',
        'Spicy Preference': 'category',
        'Allergies': 'string',
        'Consumption Size': 'category'
    })

    return users