from flask import session, redirect, url_for
from models.models import User, Product, Order, db

class AdminController:
    @staticmethod
    def login(username, password):
        admin = User.query.filter_by(username=username, is_admin=True).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_bp.dashboard'))
        return redirect(url_for('admin_bp.login'))

    @staticmethod
    def logout():
        session.pop('admin_id', None)
        return redirect(url_for('admin_bp.login'))

    @staticmethod
    def get_all_users():
        return User.query.filter_by(is_admin=False).all()

    @staticmethod
    def get_products_paginated(page, per_page):
        pagination = Product.query.paginate(page=page, per_page=per_page)
        return pagination.items, pagination.page, pagination.pages

    @staticmethod
    def add_product(name, price, image_url, description, category):
        product = Product(
            name=name,
            price=float(price),
            image_url=image_url,
            description=description,
            category=category
        )
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def get_product_by_id(pid):
        return Product.query.get(pid)

    @staticmethod
    def update_product(pid, name, price, image_url, description, category):
        product = Product.query.get(pid)
        if product:
            product.name = name
            product.price = float(price)
            product.image_url = image_url
            product.description = description
            product.category = category
            db.session.commit()

    @staticmethod
    def delete_product(pid):
        product = Product.query.get(pid)
        if product:
            db.session.delete(product)
            db.session.commit()

    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def confirm_payment(order_id):
        order = Order.query.get(order_id)
        if order and not order.is_paid:
            order.is_paid = True
            db.session.commit()
            return True
        return False