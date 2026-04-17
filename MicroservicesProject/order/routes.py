from flask import Blueprint, jsonify, request, make_response
import requests
from models import Order, OrderItem, db

order_blueprint = Blueprint('order_api_routes', __name__, url_prefix='/api/order') 

USER_API_URL = 'http://user-service-c:5001/api/user/'

def get_user(api_key):
    headers = {'Authorization': api_key}
    response = requests.get(USER_API_URL, headers=headers)
    if response.status_code != 200:
        return {'message': 'Not Authorized'}
    user = response.json()
    return user

@order_blueprint.route('/', methods=['GET'])
def get_open_order():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'API key is missing'}), 401
    response = get_user(api_key)
    user = response.get('result')
    if not user:
        return jsonify({'message': 'Not Authorized'}), 401
    open_order = Order.query.filter_by(user_id=user['id'], is_open=True).first()
    if open_order:
        return jsonify({
            'message': 'Open order retrieved',
            'order': open_order.serialize()
        }), 200
    else:
        return jsonify({'message': 'No open order found'}), 404


@order_blueprint.route('/all', methods=['GET'])
def get_all_orders():
    all_orders = Order.query.all()
    result = [order.serialize() for order in all_orders]
    response = {
        'message': 'Retrieved all orders',
        'result': result
    }
    return jsonify(response)


@order_blueprint.route('/add-item', methods=['POST'])
def add_order_item():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'API key is missing'}), 401
    response = get_user(api_key)
    if not response.get('result'):
        return jsonify({'message': 'Not Authorized'}), 401
    user = response.get('result')
    book_id = int(request.form['book_id'])
    quantity = int(request.form['quantity'])
    user_id = user['id']

    open_order = Order.query.filter_by(user_id=user_id, is_open=True).first()

    if not open_order:
        open_order = Order(user_id=user_id, is_open=True)
        order_item = OrderItem(book_id=book_id, quantity=quantity)
        open_order.order_items.append(order_item)
    else:
        found = False
        for item in open_order.order_items:
            if item.book_id == book_id:
                item.quantity += quantity
                found = True
        
        if not found:
            order_item = OrderItem(book_id=book_id, quantity=quantity)
            open_order.order_items.append(order_item)

    db.session.add(open_order)
    db.session.commit()

    return jsonify({
        'message': 'Item added to order',
        'order': open_order.serialize()
    }), 200
        

@order_blueprint.route('/checkout', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'API key is missing'}), 401
    response = get_user(api_key)
    user = response.get('result')
    if not user:
        return jsonify({'message': 'Not Authorized'}), 401
    
    open_order = Order.query.filter_by(user_id=user['id'], is_open=True).first()
    
    if open_order:
        open_order.is_open = False
        db.session.add(open_order)
        db.session.commit()
        return jsonify({'message': 'Order checked out successfully', 'result': open_order.serialize()}), 200
    else:
        return jsonify({'message': 'No open order found'}), 404