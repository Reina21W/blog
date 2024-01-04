from flask import Blueprint, render_template, request, url_for, redirect, session
from forms import RegisterForm, LoginForm
from models import UserModel
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            Password1 = form.Password1.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("The account is valid!")
                return redirect(url_for("auth.register"))
            if check_password_hash(user.password, Password1):
                session['user_id'] = user.id
                # login_user(user)
                return redirect("/")
            else:
                print("Sorry, your password is wrong!")
        else:
            print(form.errors)
        return redirect(url_for("auth.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.Password1.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return "wrong"


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
