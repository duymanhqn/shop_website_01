
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from datetime import datetime
from models.models import db, CartItem, Product, Order
import hmac, hashlib, json, requests


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

        # Nếu thanh toán COD
        if payment_method == "COD":
            new_order = Order(
                user_id=user_id,
                total_amount=total_price,
                payment_method="COD",
                status="Chờ thanh toán",
                created_at=datetime.now(),
            )
            db.session.add(new_order)
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()

            flash("Đặt hàng thành công (Thanh toán khi nhận hàng).", "success")
            return redirect(url_for("order_bp.success"))

        # Nếu thanh toán bằng MoMo
        elif payment_method == "MoMo":
            endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
            partnerCode = "MOMO"
            accessKey = "F8BBA842ECF85"
            secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
            orderInfo = "Thanh toán đơn hàng qua MoMo"

            # Chỉnh đúng URL: ipnUrl khác redirectUrl
            redirectUrl = "https://unboasting-skylar-nonsimilarly.ngrok-free.dev/order/momo_return"
            ipnUrl = "https://unboasting-skylar-nonsimilarly.ngrok-free.dev/order/momo_ipn"

            amount = str(int(total_price))
            orderId = datetime.now().strftime("%Y%m%d%H%M%S")
            requestId = orderId
            requestType = "captureWallet"

            rawSignature = f"accessKey={accessKey}&amount={amount}&extraData=&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
            signature = hmac.new(secretKey.encode('utf-8'), rawSignature.encode('utf-8'), hashlib.sha256).hexdigest()

            data = {
                "partnerCode": partnerCode,
                "accessKey": accessKey,
                "requestId": requestId,
                "amount": amount,
                "orderId": orderId,
                "orderInfo": orderInfo,
                "redirectUrl": redirectUrl,
                "ipnUrl": ipnUrl,
                "extraData": "",
                "requestType": requestType,
                "signature": signature,
            }

            res = requests.post(endpoint, json=data)
            result = res.json()
            return redirect(result["payUrl"])

    #  MoMo gửi POST về đây (IPN)
    @staticmethod
    def momo_ipn():
        data = request.get_json(silent=True) or {}
        print(" MoMo IPN:", data)

        orderId = data.get("orderId")
        resultCode = str(data.get("resultCode"))

        if resultCode == "0":
            print(f" IPN: Thanh toán thành công cho order {orderId}")
            # Ở đây chỉ log thôi, không cần tạo lại đơn
        else:
            print(f" IPN: Thanh toán thất bại {orderId}")

        return jsonify({"message": "ok"})

    # Xử lý khi MoMo redirect về trình duyệt
    @staticmethod
    def momo_return():
        resultCode = request.args.get("resultCode")
        amount = request.args.get("amount")

        # Chặn gọi lại nhiều lần (chỉ tạo order 1 lần)
        if session.get("momo_paid"):
            return redirect(url_for("order_bp.success"))

        if resultCode == "0":
            if "user_id" not in session:
                flash("Vui lòng đăng nhập!", "error")
                return redirect(url_for("auth_bp.auth"))

            user_id = session["user_id"]
            cart_items = CartItem.query.filter_by(user_id=user_id).all()
            total_price = sum(Product.query.get(i.product_id).price * i.quantity for i in cart_items)

            order = Order(
                user_id=user_id,
                total_amount=total_price,
                payment_method="MoMo",
                status="Đã thanh toán",
                created_at=datetime.now(),
            )
            db.session.add(order)
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()

            session["momo_paid"] = True  #ngăn tạo lại order lần nữa
            flash("Thanh toán MoMo thành công!", "success")
            return redirect(url_for("order_bp.success"))
        else:
            flash("Thanh toán thất bại hoặc bị hủy.", "error")
            return redirect(url_for("cart_bp.cart"))

    @staticmethod
    def success():
        # Khi vào trang này, reset lại flag
        session.pop("momo_paid", None)
        return render_template("success.html")
