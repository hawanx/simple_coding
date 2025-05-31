# server.py
from flask import Flask, render_template, request, jsonify
from gg import fetch_orders
from datetime import datetime

app = Flask(__name__)

order_dict = fetch_orders(200)
print(len(order_dict))
# start_date = datetime.strptime("2024-10-07", "%Y-%m-%d")
# end_date = datetime.strptime("2024-10-17", "%Y-%m-%d")
#
# # Calculate the sum of costs for orders within the date range
# total_cost = sum(
#     order["cost"] for order in order_dict
#     if start_date <= datetime.strptime(order["date_ordered"], "%Y-%m-%d %H:%M:%S") <= end_date
# )


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query'].lower()
    results = results = [
        order for order in order_dict
        if query in order['restaurant_name'].lower() or
           any(query in item['name'].lower() for item in order['order_items'])
    ]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

















