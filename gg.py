import requests
from app_settings import *

headers = {
    "Cookie": HEADERS_COOKIE,
    "User-Agent": HEADERS_USER_AGENT
}

order_dict = []


def fetch_orders(max_orders, last_order_id=''):
    while len(order_dict) < max_orders:
        params = {"order_id": last_order_id}
        response = requests.get(SWIGGY_URL, headers=headers, params=params)
        if response.status_code == 200:
            orders = response.json()["data"]["orders"]
            for order in orders:
                order_dict.append({
                    "order_id": order.get("order_id"),
                    "restaurant_name": order.get("restaurant_name"),
                    "order_items": [
                        {key: item[key] for key in ['name', 'quantity'] if key in item} for item in order["order_items"]
                    ],
                    "cost": order["order_total"],
                    "date_ordered": order["order_time"],
                    "restaurant_rating": order["rating_meta"]["restaurant_rating"]["rating"]
                })
            last_order_id = str(orders[-1]["order_id"])
        else:
            print(f"Request failed at order_dict length = {len(order_dict)} with status code {response.status_code}.")
            print(response.text)  # Print the error message if any
            break
    return order_dict
