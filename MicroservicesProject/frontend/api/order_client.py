import requests
from . import ORDER_API_URL
from flask import session


class OrderClient:
    @staticmethod
    def get_order():
        header = {'Authorization': session['user_api_key']}

        response = requests.get(ORDER_API_URL + '/api/order/', headers=header)
        if response.ok:
            return response.json()
        return None

    @staticmethod
    def add_to_cart(book_id, quantity=1):
        payload = {
            'book_id': book_id,
            'quantity': quantity
        }
        header = {'Authorization': session['user_api_key']}

        response = requests.post(ORDER_API_URL + '/api/order/add-item',
                                 data=payload,
                                 headers=header)
        if response.ok:
            return response.json()
        return None

    @staticmethod
    def checkout():
        header = {'Authorization': session['user_api_key']}
        response = requests.post(ORDER_API_URL + '/api/order/checkout', headers=header)
        if response.ok:
            return response.json()
        return None

    @staticmethod
    def get_order_from_session():
        default_order = {
            'items': {}
        }
        return session.get('order', default_order)
