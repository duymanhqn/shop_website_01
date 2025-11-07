from flask import Blueprint, request
from controllers.order_controller import OrderController

order_bp = Blueprint("order_bp", __name__)

@order_bp.route("/checkout")
def checkout():
    return OrderController.checkout()

@order_bp.route("/confirm_order", methods=["POST"])
def confirm_order():
    payment_method = request.form.get("payment_method")
    return OrderController.confirm_order(payment_method)

@order_bp.route("/confirm_bank/<int:order_id>", methods=["POST"])
def confirm_bank(order_id):
    return OrderController.confirm_bank(order_id)

@order_bp.route("/success")
def success():
    return OrderController.success()
