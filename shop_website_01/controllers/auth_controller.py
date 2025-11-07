from flask import session, flash, redirect, url_for
from models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


class AuthController:
    @staticmethod
    def register(fullname, gmail, username, password):
        existing_user = User.query.filter_by(username=username).first()
        existing_mail = User.query.filter_by(gmail=gmail).first()

        if existing_user:
            flash("Tên đăng nhập đã tồn tại!", "error")
            return False
        if existing_mail:
            flash("Gmail này đã được sử dụng!", "error")
            return False

        hashed_password = generate_password_hash(password)

        new_user = User(
            fullname=fullname,
            gmail=gmail,
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Đăng ký thành công! Mời bạn đăng nhập.", "success")
        return True

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()

        if user and (user.password == password or check_password_hash(user.password, password)):
            session["user_id"] = user.id
            session["user_name"] = user.fullname
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("home_bp.home"))
        else:
            flash("Sai tài khoản hoặc mật khẩu!", "error")
            return redirect(url_for("auth_bp.auth"))

    @staticmethod
    def logout():
        session.clear()
        flash("Đã đăng xuất thành công!", "info")
        return redirect(url_for("home_bp.home"))
