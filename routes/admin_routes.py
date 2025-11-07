from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from controllers.admin_controller import AdminController
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

# ==================== LOGIN / LOGOUT ====================

@admin_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return AdminController.login(username, password)
    return render_template("admin_login.html")


@admin_bp.route("/dashboard")
def dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_bp.login"))
    users = AdminController.get_all_users()
    return render_template("admin_dashboard.html", users=users)


@admin_bp.route("/logout")
def logout():
    return AdminController.logout()


# ==================== QUẢN LÍ HÀNG HÓA ====================

@admin_bp.route("/products")
def products():
    if "admin_id" not in session:
        return redirect(url_for("admin_bp.login"))

    #  Lấy số trang hiện tại (mặc định là 1)
    page = request.args.get("page", 1, type=int)

    #  Lấy 8 sản phẩm mỗi trang
    products, current_page, total_pages = AdminController.get_products_paginated(page, per_page=8)

    return render_template(
        "admin_products.html",
        products=products,
        current_page=current_page,
        total_pages=total_pages
    )



#  Thêm sản phẩm (có upload ảnh)
@admin_bp.route("/products/add", methods=["POST"])
def add_product():
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]
    category = request.form["category"]

    image_file = request.files.get("image_file")
    image_url = None
    if image_file and image_file.filename != "":
        filename = secure_filename(image_file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        image_file.save(save_path)
        image_url = f"uploads/{filename}"

    AdminController.add_product(name, price, image_url, description, category)
    flash("✅ Đã thêm sản phẩm mới!", "success")
    return redirect(url_for("admin_bp.products"))


#  Trang sửa sản phẩm
@admin_bp.route("/products/edit/<int:pid>")
def edit_product(pid):
    product = AdminController.get_product_by_id(pid)
    if not product:
        flash(" Không tìm thấy sản phẩm!", "danger")
        return redirect(url_for("admin_bp.products"))
    return render_template("admin_edit_product.html", product=product)


# Cập nhật sản phẩm
@admin_bp.route("/products/update/<int:pid>", methods=["POST"])
def update_product(pid):
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]
    category = request.form["category"]

    image_file = request.files.get("image_file")
    image_url = request.form.get("current_image")

    if image_file and image_file.filename != "":
        filename = secure_filename(image_file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        image_file.save(save_path)
        image_url = f"uploads/{filename}"

    AdminController.update_product(pid, name, price, image_url, description, category)
    flash(" Đã cập nhật sản phẩm!", "info")
    return redirect(url_for("admin_bp.products"))


#  Xóa sản phẩm
@admin_bp.route("/products/delete/<int:pid>")
def delete_product(pid):
    AdminController.delete_product(pid)
    flash(" Đã xóa sản phẩm!", "warning")
    return redirect(url_for("admin_bp.products"))



@admin_bp.route("/orders")
def orders():
    if "admin_id" not in session:
        return redirect(url_for("admin_bp.login"))

    orders = AdminController.get_all_orders()
    return render_template("admin_orders.html", orders=orders)
@admin_bp.route("/orders/confirm/<int:order_id>")
def confirm_order(order_id):
    if "admin_id" not in session:
        return redirect(url_for("admin_bp.login"))

    if AdminController.confirm_payment(order_id):
        flash(" Đã xác nhận thanh toán đơn hàng!", "success")
    else:
        flash(" Không thể xác nhận (đơn hàng đã thanh toán hoặc không tồn tại).", "warning")

    return redirect(url_for("admin_bp.orders"))
