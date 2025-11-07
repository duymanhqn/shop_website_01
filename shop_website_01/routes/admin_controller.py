from flask import session, flash, redirect, url_for
from models.models import db, Admin, User, Product, Order
from datetime import datetime


class AdminController:

    # Đăng nhập admin
    @staticmethod
    def login(username, password):
        
        admin = Admin.query.filter_by(usernamead=username, password=password).first()
        if admin:
            session["admin_id"] = admin.id           
            session["admin_name"] = admin.fullnamead
            
            return redirect(url_for("admin_bp.dashboard"))
        else:
            flash("Sai tài khoản hoặc mật khẩu admin!", "error")
            return redirect(url_for("admin_bp.login"))

    # Đăng xuất admin
    @staticmethod
    def logout():
        session.pop("admin_id", None)
        session.pop("admin_name", None)
        return redirect(url_for("admin_bp.login"))


    # Lấy danh sách người dùng
    @staticmethod
    def get_all_users():
        return User.query.all()

    # Lấy danh sách sản phẩm
    @staticmethod
    def get_all_products():
        return Product.query.all()

    # Thêm sản phẩm mới
    @staticmethod
    def add_product(name, price, image_url, description, category):
        new_product = Product(
            name=name,
            price=price,
            image_url=image_url,
            description=description,
            category=category
        )
        db.session.add(new_product)
        db.session.commit()

    # Cập nhật sản phẩm
    @staticmethod
    def update_product(pid, name, price, image_url, description, category):
        product = Product.query.get(pid)
        if product:
            product.name = name
            product.price = price
            product.image_url = image_url
            product.description = description
            product.category = category
            db.session.commit()

    # Xóa sản phẩm
    @staticmethod
    def delete_product(pid):
        product = Product.query.get(pid)
        if product:
            db.session.delete(product)
            db.session.commit()

    # Lấy sản phẩm theo ID
    @staticmethod
    def get_product_by_id(pid):
        return Product.query.get(pid)

    # Phân trang sản phẩm
    @staticmethod
    def get_products_paginated(page=1, per_page=8):
        pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.page, pagination.pages

    # Lấy toàn bộ đơn hàng (JOIN với bảng user)
    @staticmethod
    def get_all_orders():
        results = db.session.query(
            Order.id,
            User.fullname,
            Order.total_amount,
            Order.payment_method,
            Order.status,
            Order.bank_account
        ).join(User, User.id == Order.user_id).all()
        return results

    # Xác nhận thanh toán đơn hàng
    @staticmethod
    def confirm_payment(order_id):
        """Cập nhật đơn hàng từ 'Chờ thanh toán' -> 'Đã thanh toán'"""
        order = Order.query.get(order_id)
        if order and order.status == "Chờ thanh toán":
            order.status = "Đã thanh toán"
            order.paid_at = datetime.now()
            db.session.commit()
            return True
        return False
