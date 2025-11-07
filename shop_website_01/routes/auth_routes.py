from flask import Blueprint, render_template, request
from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "register":
            fullname = request.form["fullname"]
            gmail = request.form["gmail"]
            username = request.form["username"]
            password = request.form["password"]
            AuthController.register(fullname, gmail, username, password)
        elif form_type == "login":
            username = request.form["username"]
            password = request.form["password"]
            return AuthController.login(username, password)
    return render_template("auth.html")

#  Route logout
@auth_bp.route("/logout")
def logout():
    return AuthController.logout()
