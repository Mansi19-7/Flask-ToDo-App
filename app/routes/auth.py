from flask import Blueprint, render_template, request,redirect, url_for, flash, session
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from app import db  

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        contactNo = request.form.get("contactNo")
        gender = request.form.get("gender")
        fields = request.form.getlist("field")

        print("Username:", repr(username))
        print("Password:", repr(password))
        print("Email:", repr(email))
        print("Contact:", repr(contactNo))
        print("Gender:", repr(gender))
        print("Fields:", repr(fields))
        
        if not username or not password or not email or not contactNo or not gender or not fields:
            flash("Please fill all required fields!", "danger")
            return redirect(url_for("auth.registration"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.registration"))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already registered!", "danger")
            return redirect(url_for("auth.registration"))

        existing_contactNo = User.query.filter_by(contact_no=contactNo).first()
        if existing_contactNo:
            flash("contact No. already registered!", "danger")
            return redirect(url_for("auth.registration"))

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            contact_no=contactNo,
            gender=gender,
            field=",".join(fields)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter username and password!", "danger")
            return redirect(url_for("auth.login"))
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            session["user_id"] = user.id
            flash("Login successfully", "success")
            return redirect(url_for("task.view_task"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")
            
@auth_bp.route("/logout")
def logout() :
    session.pop("user", None)
    session.pop("user_id", None)
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))
