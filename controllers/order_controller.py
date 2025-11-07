# controllers/order_controller.py
from flask import render_template, session, redirect, url_for, flash
from datetime import datetime
from urllib.parse import quote
from models.models import db, CartItem, Product, Order

def build_vietqr_url(bank_code: str, account: str, amount: int, add_info: str, account_name: str) -> str:
    base = f"https://img.vietqr.io/image/{bank_code}-{account}-compact2.png"
    return f"{base}?amount={int(amount)}&addInfo={quote(add_info)}&accountName={quote(account_name)}"


class OrderController:
    
    # Trang thanh toán (hiển thị giỏ hàng)
    
    @staticmethod
    def checkout():
        if "user_id" not in session:
            return redirect(url_for("auth_bp.auth"))

        user_id = session["user_id"]
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            flash("Giỏ hàng của bạn đang trống!", "error")
            return redirect(url_for("cart_bp.cart"))

        total = 0
        for item in cart_items:
            product = Product.query.get(item.product_id)
            item.product = product
            item.total_price = product.price * item.quantity
            total += item.total_price

        return render_template("checkout.html", cart_items=cart_items, total=total)

    
    # Xử lý khi chọn phương thức thanh toán
    
    @staticmethod
    def confirm_order(payment_method):
        if "user_id" not in session:
            return redirect(url_for("auth_bp.auth"))

        user_id = session["user_id"]
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            flash("Không có sản phẩm nào để thanh toán!", "error")
            return redirect(url_for("cart_bp.cart"))

        total_price = sum(Product.query.get(i.product_id).price * i.quantity for i in cart_items)
        transfer_note = f"TT{datetime.now().strftime('%Y%m%d%H%M%S')} - MHTHM"

        # COD
        if payment_method == "COD":
            new_order = Order(
                user_id=user_id,
                total_amount=total_price,
                payment_method="COD",
                status="Chờ thanh toán",
                created_at=datetime.now()
            )
            db.session.add(new_order)
            db.session.commit()

            
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()

            flash("Đặt hàng thành công (Thanh toán khi nhận hàng).", "success")
            return redirect(url_for("order_bp.success"))

        # chuyển khoản 
        temp_order = Order(
            user_id=user_id,
            total_amount=total_price,
            payment_method="Bank",
            status="Chờ xác nhận chuyển khoản",
            bank_name="VCB",
            bank_account="9962560330",
            bank_account_name="DOAN THANH TUYEN",
            transfer_note=transfer_note,
        )

        qr_url = build_vietqr_url(
            bank_code=temp_order.bank_name,
            account=temp_order.bank_account,
            amount=int(temp_order.total_amount),
            add_info=temp_order.transfer_note,
            account_name=temp_order.bank_account_name,
        )

        
        return render_template("bank_payment.html", order=temp_order, qr_url=qr_url)

    
    # Khi nhấn nút "Tôi đã chuyển khoản"
    
    @staticmethod
    def confirm_bank(order_id):
        user_id = session.get("user_id")
        if not user_id:
            flash("Vui lòng đăng nhập!", "error")
            return redirect(url_for("auth_bp.auth"))

        
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            flash("Không tìm thấy sản phẩm trong giỏ!", "error")
            return redirect(url_for("cart_bp.cart"))

        total_price = sum(Product.query.get(i.product_id).price * i.quantity for i in cart_items)
        transfer_note = f"TT{datetime.now().strftime('%Y%m%d%H%M%S')} - MHTHM"

        order = Order(
            user_id=user_id,
            total_amount=total_price,
            payment_method="Bank",
            status="Đã thanh toán",
            bank_name="VCB",
            bank_account="9962560330",
            bank_account_name="DOAN THANH TUYEN",
            transfer_note=transfer_note,
            paid_at=datetime.now(),
        )

        db.session.add(order)

        
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()

        flash("Cảm ơn bạn! Hệ thống đã nhận xác nhận chuyển khoản.", "success")
        return redirect(url_for("order_bp.success"))

    
    # Trang thông báo thanh toán thành công
    
    @staticmethod
    def success():
        return render_template("success.html")
