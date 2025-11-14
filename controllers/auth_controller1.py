from flask import session, flash, redirect, url_for, render_template, request
from models.models import db, User, OtpRegister
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from utils.send_email import send_otp_email
import random


class AuthController:

    # =============================================
    # 1) ĐĂNG KÝ → GỬI OTP
    # =============================================
    @staticmethod
    def register(fullname, gmail, username, password):
        existing_user = User.query.filter_by(username=username).first()
        existing_mail = User.query.filter_by(gmail=gmail).first()

        if existing_user:
            flash("Tên đăng nhập đã tồn tại!", "error")
            return redirect(url_for("auth_bp.auth"))
        if existing_mail:
            flash("Gmail này đã được sử dụng!", "error")
            return redirect(url_for("auth_bp.auth"))

        # Tạo OTP
        otp_code = str(random.randint(100000, 999999))
        expire_at = datetime.utcnow() + timedelta(minutes=5)

        otp_entry = OtpRegister(
            email=gmail,
            otp_code=otp_code,
            expire_at=expire_at,
            is_verified=False
        )
        db.session.add(otp_entry)
        db.session.commit()

        # Gửi mail OTP
        send_otp_email(gmail, otp_code)

        # Lưu thông tin tạm
        session["pending_user"] = {
            "fullname": fullname,
            "gmail": gmail,
            "username": username,
            "password": password
        }

        # Dùng trang OTP chung
        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_register"),
            resend_url=url_for("auth_bp.resend_otp")
        )


    # =============================================
    # 2) XÁC MINH OTP ĐĂNG KÝ
    # =============================================
    @staticmethod
    def verify_register_otp(otp_input):
        pending = session.get("pending_user")

        if not pending:
            flash("Không tìm thấy thông tin đăng ký!", "error")
            return redirect(url_for("auth_bp.auth"))

        gmail = pending["gmail"]

        otp_record = (
            OtpRegister.query.filter_by(email=gmail, is_verified=False)
            .order_by(OtpRegister.id.desc())
            .first()
        )

        if not otp_record:
            flash("Không tìm thấy mã OTP!", "error")
            return redirect(url_for("auth_bp.verify_register_page"))

        if otp_record.expire_at < datetime.utcnow():
            flash("OTP đã hết hạn!", "error")
            return redirect(url_for("auth_bp.auth"))

        if otp_input != otp_record.otp_code:
            flash("Mã OTP không đúng!", "error")
            return redirect(url_for("auth_bp.verify_register_page"))

        otp_record.is_verified = True
        db.session.commit()

        hashed_password = generate_password_hash(pending["password"])

        new_user = User(
            fullname=pending["fullname"],
            gmail=pending["gmail"],
            username=pending["username"],
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        session.pop("pending_user", None)

        flash("Đăng ký thành công! Mời bạn đăng nhập.", "success")
        return redirect(url_for("auth_bp.auth"))


    # =============================================
    # 3) LOGIN
    # =============================================
    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()

        if user and (user.password == password or check_password_hash(user.password, password)):
            session["user_id"] = user.id
            session["user_name"] = user.fullname
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("home_bp.home"))

        flash("Sai tài khoản hoặc mật khẩu!", "error")
        return redirect(url_for("auth_bp.auth"))


    # =============================================
    # 4) LOGOUT
    # =============================================
    @staticmethod
    def logout():
        session.clear()
        flash("Đã đăng xuất thành công!", "info")
        return redirect(url_for("home_bp.home"))


    # =============================================
    # 5) RESEND OTP ĐĂNG KÝ
    # =============================================
    @staticmethod
    def resend_otp():
        pending = session.get("pending_user")

        if not pending:
            flash("Không tìm thấy thông tin đăng ký!", "error")
            return redirect(url_for("auth_bp.auth"))

        gmail = pending["gmail"]

        otp_code = str(random.randint(100000, 999999))
        expire_at = datetime.utcnow() + timedelta(minutes=5)

        otp_entry = OtpRegister(
            email=gmail,
            otp_code=otp_code,
            expire_at=expire_at,
            is_verified=False
        )
        db.session.add(otp_entry)
        db.session.commit()

        send_otp_email(gmail, otp_code)

        flash("Đã gửi mã OTP mới!", "success")

        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_register"),
            resend_url=url_for("auth_bp.resend_otp")
        )


    # =============================================
    # 6) QUÊN MẬT KHẨU → GỬI OTP
    # =============================================
    @staticmethod
    def forgot_password():
        if request.method == "GET":
            return render_template("forgot_password.html")

        gmail = request.form.get("gmail")
        user = User.query.filter_by(gmail=gmail).first()

        if not user:
            flash("Email không tồn tại!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        otp_code = str(random.randint(100000, 999999))
        expire_at = datetime.utcnow() + timedelta(minutes=5)

        otp_entry = OtpRegister(
            email=gmail,
            otp_code=otp_code,
            expire_at=expire_at,
            is_verified=False
        )
        db.session.add(otp_entry)
        db.session.commit()

        send_otp_email(gmail, otp_code)

        session["reset_gmail"] = gmail

        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_forgot"),
            resend_url=url_for("auth_bp.resend_forgot_otp")
        )


    # =============================================
    # 7) XÁC MINH OTP QUÊN MẬT KHẨU
    # =============================================
    @staticmethod
    def verify_forgot_otp(otp_input):
        gmail = session.get("reset_gmail")

        if not gmail:
            flash("Phiên làm việc đã hết!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        otp_record = (
            OtpRegister.query.filter_by(email=gmail, is_verified=False)
            .order_by(OtpRegister.id.desc())
            .first()
        )

        if not otp_record:
            flash("Không tìm thấy OTP!", "error")
            return redirect(url_for("auth_bp.verify_forgot_page"))

        if otp_record.expire_at < datetime.utcnow():
            flash("OTP đã hết hạn!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        if otp_input != otp_record.otp_code:
            flash("Mã OTP không đúng!", "error")
            return redirect(url_for("auth_bp.verify_forgot_page"))

        otp_record.is_verified = True
        db.session.commit()

        return redirect(url_for("auth_bp.reset_password"))


    # =============================================
    # 8) RESEND OTP QUÊN MẬT KHẨU
    # =============================================
    @staticmethod
    def resend_forgot_otp():
        gmail = session.get("reset_gmail")

        if not gmail:
            flash("Phiên làm việc đã hết!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        otp_code = str(random.randint(100000, 999999))
        expire_at = datetime.utcnow() + timedelta(minutes=5)

        otp_entry = OtpRegister(
            email=gmail,
            otp_code=otp_code,
            expire_at=expire_at
        )
        db.session.add(otp_entry)
        db.session.commit()

        send_otp_email(gmail, otp_code)

        flash("OTP mới đã được gửi!", "success")

        return render_template(
            "verify_otp.html",
            action_url=url_for("auth_bp.verify_forgot"),
            resend_url=url_for("auth_bp.resend_forgot_otp")
        )


    # =============================================
    # 9) ĐẶT LẠI MẬT KHẨU
    # =============================================
    @staticmethod
    def reset_password():
        if request.method == "GET":
            return render_template("reset_password.html")

        new_pass = request.form.get("password")
        gmail = session.get("reset_gmail")

        if not gmail:
            flash("Phiên làm việc đã hết!", "error")
            return redirect(url_for("auth_bp.forgot_password"))

        user = User.query.filter_by(gmail=gmail).first()
        user.password = generate_password_hash(new_pass)
        db.session.commit()

        session.pop("reset_gmail", None)

        flash("Đổi mật khẩu thành công!", "success")
        return redirect(url_for("auth_bp.auth"))
