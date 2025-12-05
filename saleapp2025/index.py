import pdb
from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
import dao
from saleapp2025.dao import get_product_by_id
from saleapp2025 import app, login_manager, admin, db
import math
from flask_login import login_user, logout_user, login_required, current_user
import cloudinary.uploader


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')
    prods = dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_product() / app.config["PAGE_SIZE"])
    return render_template('index.html', prods=prods, pages=pages)


@app.route("/products/<int:id>")
def details(id):
    prod = get_product_by_id(id)
    return render_template("product-details.html", prod=prod)


@app.route("/login", methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = 'Tài khoản hoặc mật khẩu không đúng!'
    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route("/register", methods=['get', 'post'])
def register_my_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # import pdb
        # pdb.set_trace()
        if password.__eq__(confirm_password):
            name = request.form.get('name')
            username = request.form.get('username')
            avatar = request.files.get('avatar')
            path_file = None
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                path_file = res['secure_url']
            try:
                dao.add_user(name, username, password, path_file)
                return redirect("/login")
            except:
                db.session.rollback()
                err_msg = "Hệ thống đang gặp sự cố. Vui long quay lại sau."
        else:
            err_msg = "Mật khẩu không trùng khớp! Nhập lại."
    return render_template("register.html", err_msg=err_msg)


@login_manager.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }


@app.route("/admin-login", methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)
    if user:
        login_user(user)
        return redirect('/admin')
    else:
        err_msg = 'Tài khoản hoặc mật khẩu không đúng!'


@app.route('/cart')
def cart():
    session['cart'] = {
        "1": {
            "id": 101,
            "name": "ASUS TUF Gaming F16",
            "price": 21290000,
            "quantity": 2,
            "image": "https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/t/e/text_d_i_7_36.png",
        },
        "2": {
            "id": 102,
            "name": "ASUS VivoBook Go 14",
            "price": 22990000,
            "quantity": 1,
            "image": "https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/t/e/text_ng_n_-_2023-06-08t005130.908.png",
        }
    }

    total_quantity = 0
    total_amount = 0

    if 'cart' in session:
        for item in session['cart'].values():
            total_quantity += item['quantity']
            total_amount += item['quantity'] * item['price']
    stats = {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }
    return render_template('cart.html', stats=stats)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
