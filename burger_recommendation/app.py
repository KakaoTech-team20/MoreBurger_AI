from flask import Flask, render_template, jsonify
import pandas as pd
import os
from burger_recommendation import recommend_burgers, load_and_preprocess_data, load_user_data

app = Flask(__name__)

burgers = load_and_preprocess_data('data/burgers_data.csv')
users = load_user_data('data/user_data.csv')


@app.route('/')
def index():
    return render_template('index.html', users=users.to_dict('records'))


@app.route('/recommend/<int:user_id>')
def recommend(user_id):
    try:
        user = users[users['UserID'] == user_id].iloc[0]
        user_dict = user.to_dict()
        # user_dict['Previous Orders'] = eval(user_dict['Previous Orders'])

        previous_orders = []
        for order_id in user_dict['Previous Orders']:
            burger = burgers[burgers['ID'] == order_id].iloc[0]
            previous_orders.append(f"{burger['Name']}({order_id})")
        user_dict['Previous Orders'] = previous_orders

        recommended_burgers = recommend_burgers(user, burgers)

        if recommended_burgers.empty:
            return jsonify({'user': user_dict, 'burgers': []})

        result = recommended_burgers[['ID', 'Name', 'Price', 'Similarity', 'Priority', 'spicy']].to_dict('records')
        for burger in result:
            image_path = f"static/images/burger_images/image_{burger['ID']}.png"
            if os.path.exists(image_path):
                burger['image'] = f"/static/images/burger_images/image_{burger['ID']}.png"
            else:
                burger['image'] = "/static/images/burger_images/default.webp"
            burger['order_count'] = user_dict['Previous Orders'].count(f"{burger['Name']}({burger['ID']})")

        # 순서대로 정렬
        result = sorted(result, key=lambda x: (-x['Priority'], -x['Similarity']))
        for i, burger in enumerate(result, 1):
            burger['rank'] = i

        return jsonify({'user': user_dict, 'burgers': result})
    except Exception as e:
        app.logger.error(f"Error in recommend function: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
