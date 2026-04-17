from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from flask_login import current_user

import forms
from api.book_client import BookClient
from api.user_api import UserClient
from api.order_client import OrderClient

blueprint = Blueprint('frontend', __name__)


@blueprint.context_processor
def cart_count():
    count = 0
    order = session.get('order')
    if order:
        for item in order.get('order_items', []):
            count += item['quantity']

    return {'cart_items': count}


@blueprint.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_from_session()
    try:
        books = BookClient.get_books()
    except:
        books = {'result': []}

    return render_template('index.html', books=books)


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = forms.RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data

            if UserClient.user_exists(username):
                flash("Please try another user name")
                return render_template('register.html', form=form)
            else:
                user = UserClient.create_user(form)
                if user:
                    flash("Registered. Please login.")
                    return redirect(url_for('frontend.index'))
        else:
            flash("Errors")

    return render_template('register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_key = UserClient.login(form)
            if api_key:
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                if user and user.get('result'):
                    session['user'] = user['result']
                else:
                    session['user'] = {'username': form.username.data, 'api_key': api_key}

                try:
                    order = OrderClient.get_order()
                    if order and order.get('order'):
                        session['order'] = order['order']
                except Exception:
                    session.pop('order', None)

                flash('Welcome back')
                return redirect(url_for('frontend.index'))
            else:
                flash('Cannot Login')
        else:
            flash('Cannot Login')

    return render_template('login.html', form=form)


@blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('frontend.index'))


@blueprint.route('/book/<slug>', methods=['GET', 'POST'])
def book_details(slug):
    response = BookClient.get_book(slug)
    book = response['result']

    form = forms.ItemForm(book_id=book['id'])

    if request.method == 'POST':
        if 'user' not in session:
            flash("Please Login")
            return redirect(url_for('frontend.login'))

        order = OrderClient.add_to_cart(book_id=book['id'], quantity=1)
        print(order)
        if order and order.get('order'):
            session['order'] = order['order']
            flash("Book added to the cart")
        else:
            flash("Could not add book to the cart")

    return render_template('book_info.html', book=book, form=form)


@blueprint.route('/checkout', methods=['GET'])
def checkout():
    if 'user' not in session:
        flash('Please login')
        return redirect(url_for('frontend.login'))

    if 'order' not in session:
        flash("Please add some books to the cart")
        return redirect(url_for("frontend.index"))

    order = OrderClient.get_order()

    if not order or not order.get('order') or len(order['order'].get('order_items', [])) == 0:
        flash("Please add some books to the cart")
        return redirect(url_for("frontend.index"))

    checkout_result = OrderClient.checkout()
    if not checkout_result:
        flash("Checkout failed")
        return redirect(url_for("frontend.index"))

    return redirect(url_for('frontend.thank_you'))


@blueprint.route('/thank-you', methods=['GET'])
def thank_you():
    if 'user' not in session:
        flash('Please login')
        return redirect(url_for('frontend.login'))

    if 'order' not in session:
        flash("Please add some books to the cart")
        return redirect(url_for("frontend.index"))

    session.pop('order', None)
    flash("Your order is processing.")

    return render_template('thankyou.html')
