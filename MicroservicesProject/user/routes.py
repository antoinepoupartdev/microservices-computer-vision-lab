from flask import Blueprint, app, jsonify, request, make_response
from models import User, db
from flask_login import UserMixin, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/api/user')

@user_blueprint.route("/all", methods=["GET"])
def get_all_users():
    all_user = User.query.all()
    result = [user.selrialize() for user in all_user]
    reponse = {
        'message' : 'All users retrieved successfully',
        'result' : result
    }
    return jsonify(reponse)

@user_blueprint.route("/create", methods=["POST"])
def create_user():
    try:
        user = User()
        user.username = request.form["username"]
        user.password = generate_password_hash(request.form["password"])
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
    
        respone = ({'message' : 'User created', 'result' : user.selrialize()})
    except Exception as e:
        print(str(e))
        respone = ({'message' : 'User creation failed'})
    return jsonify(respone)

@user_blueprint.route('/login', methods=['POST'])
def login():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            response = {'message': 'User not found'}
            return make_response(jsonify({'message': 'User not found'}), 401)
        if check_password_hash(user.password, password):
            user.update_api_key()
            db.session.commit()
            login_user(user)
            
            response = {'message': 'Login successful', 'api_key': user.api_key}
            return make_response(jsonify(response), 200)
        
        response = {'message': 'Acces denied'}
        return make_response(jsonify(response), 401)
    
    
@user_blueprint.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        response = {'message': 'Logout successful'}
        return make_response(jsonify(response))
    return jsonify({'message': 'User not authenticated'}), 401


@user_blueprint.route('/<username>/exists', methods=['GET'])
def check_user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'result': True}), 200
    return jsonify({'result': False}), 404

@user_blueprint.route('/', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'result': current_user.selrialize()}), 200
    else: 
        return jsonify({'message': 'User not authenticated'}), 401
