# server.py
from flask import Flask, render_template, request, jsonify
from gg import fetch_orders

app = Flask(__name__)

order_dict = fetch_orders(200)
print(len(order_dict))
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

















