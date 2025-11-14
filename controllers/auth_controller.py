from flask import render_template, request, redirect, url_for, flash, session
# from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User
from utils.otp_helper import generate_or_update_otp, verify_otp
from utils.send_email import send_otp_email
import random


class AuthController:

    #   ĐĂNG KÝ → GỬI OTP

    @staticmethod
    def register(fullname, gmail, username, password):
        if User.query.filter_by(username=username).first():
            flash("Tên đăng nhập đã tồn tại!", "error")
            return redirect(url_for("auth_bp.auth"))

        if User.query.filter_by(gmail=gmail).first():
            flash("Gmail đã được sử dụng!", "error")
            return redirect(url_for("auth_bp.auth"))

        # Gửi OTP qua helper
        generate_or_update_otp(gmail)

        # Lưu thông tin tạm
        session["pending_user"] = {
            "fullname": fullname,
            "gmail": gmail,
            "username": username,
            "password": password,
        }

        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_register"),
            resend_url=url_for("auth_bp.resend_otp"),
        )

    #  VERIFY OTP ĐĂNG KÝ

    @staticmethod
    def verify_register_otp(otp_input):
        pending = session.get("pending_user")

        if not pending:
            flash("Không tìm thấy dữ liệu đăng ký!", "error")
            return redirect(url_for("auth_bp.auth"))

        gmail = pending["gmail"]

        if not verify_otp(gmail, otp_input):
            flash("OTP không đúng hoặc đã hết hạn!", "error")
            return redirect(url_for("auth_bp.verify_register_page"))

        # Tạo user
        user = User(
            fullname=pending["fullname"],
            gmail=pending["gmail"],
            username=pending["username"],
            password=pending["password"],
            # password=generate_password_hash(pending["password"]),
        )

        db.session.add(user)
        db.session.commit()

        session.pop("pending_user", None)

        flash("Đăng ký thành công!", "success")
        return redirect(url_for("auth_bp.auth"))

    #  GỬI LẠI OTP ĐĂNG KÝ

    @staticmethod
    def resend_otp():
        pending = session.get("pending_user")

        if not pending:
            flash("Không tìm thấy dữ liệu đăng ký!", "error")
            return redirect(url_for("auth_bp.auth"))

        result = generate_or_update_otp(pending["gmail"])

        if not result:
            flash("Bạn chỉ được gửi lại OTP sau 60 giây!", "error")
        else:
            flash("OTP mới đã được gửi!", "success")

        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_register"),
            resend_url=url_for("auth_bp.resend_otp"),
        )


    #  LOGIN
   
    # @staticmethod
    # def login(username, password):
    #     user = User.query.filter_by(username=username).first()

    #     if not user or not check_password_hash(user.password, password):
    #         flash("Sai tài khoản hoặc mật khẩu!", "error")
    #         return redirect(url_for("auth_bp.auth"))

    #     session["user_id"] = user.id
    #     return redirect(url_for("home_bp.home"))
    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()

        if not user or user.password != password:   # So sánh trực tiếp
            flash("Sai tài khoản hoặc mật khẩu!", "error")
            return redirect(url_for("auth_bp.auth"))

        session["user_id"] = user.id
        return redirect(url_for("home_bp.home"))
    #  LOGOUT
   
    @staticmethod
    def logout():
        session.clear()
        return redirect(url_for("auth_bp.auth"))

    #  QUÊN MẬT KHẨU
 
    @staticmethod
    def forgot_password():
        if request.method == "GET":
            return render_template("forgot_password.html")

        gmail = request.form.get("gmail")

        if not User.query.filter_by(gmail=gmail).first():
            flash("Email không tồn tại!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        generate_or_update_otp(gmail)
        session["reset_gmail"] = gmail

        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_forgot"),
            resend_url=url_for("auth_bp.resend_forgot_otp"),
        )

    #  VERIFY FORGOT OTP
   
    @staticmethod
    def verify_forgot_otp(otp_input):
        gmail = session.get("reset_gmail")

        if not gmail:
            flash("Phiên đã hết hạn!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        if not verify_otp(gmail, otp_input):
            flash("OTP không đúng hoặc đã hết hạn!", "error")
            return redirect(url_for("auth_bp.verify_forgot_page"))

        return redirect(url_for("auth_bp.reset_password"))

    # GỬI LẠI OTP QUÊN MẬT KHẨU

    @staticmethod
    def resend_forgot_otp():
        gmail = session.get("reset_gmail")

        if not gmail:
            flash("Phiên đã hết hạn!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        generate_or_update_otp(gmail)
        flash("OTP đã được gửi lại!", "success")

        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_forgot"),
            resend_url=url_for("auth_bp.resend_forgot_otp"),
        )
    #  RESET PASSWORD
    @staticmethod
    def reset_password():
        if request.method == "GET":
            return render_template("reset_password.html")

        gmail = session.get("reset_gmail")

        if not gmail:
            flash("Phiên đã hết hạn!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        new_pass = request.form.get("password")
        user = User.query.filter_by(gmail=gmail).first()

        user.password = generate_password_hash(new_pass)
        db.session.commit()

        session.pop("reset_gmail", None)

        flash("Đổi mật khẩu thành công!", "success")
        return redirect(url_for("auth_bp.auth"))
