from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from extensions import db, login_manager

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import User, Ticket
from forms import RegisterForm, LoginForm


# --------------------
# APP INITIALIZATION
# --------------------
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


# --------------------
# USER LOADER
# --------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --------------------
# HOME DASHBOARD
# --------------------
@app.route("/")
@login_required
def home():

    # ADMIN VIEW
    if current_user.role == "admin":
        tickets = Ticket.query.all()
        return render_template("admin_dashboard.html", tickets=tickets)

    # NORMAL USER VIEW
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tickets=tickets)

# --------------------
# REGISTER
# --------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


# --------------------
# ADMIN DASHBOARD
# --------------------
@app.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("home"))

    tickets = Ticket.query.all()

    return render_template("admin_dashboard.html", tickets=tickets)

# --------------------
# UPDATE TICKET STATUS
# --------------------
@app.route("/update-status/<int:ticket_id>/<status>")
@login_required
def update_status(ticket_id, status):

    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("home"))

    ticket = Ticket.query.get_or_404(ticket_id)

    ticket.status = status

    db.session.commit()

    flash("Ticket status updated")

    return redirect(url_for("admin_dashboard"))

# --------------------
# ASSIGN TECHNICIAN
# --------------------
@app.route("/assign-technician/<int:ticket_id>", methods=["POST"])
@login_required
def assign_technician(ticket_id):

    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("home"))

    ticket = Ticket.query.get_or_404(ticket_id)

    technician_name = request.form.get("technician")

    ticket.technician = technician_name

    db.session.commit()

    flash("Technician assigned successfully")

    return redirect(url_for("admin_dashboard"))

# --------------------
# LOGIN
# --------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user)

            flash("Login successful")

            return redirect(url_for("home"))

        flash("Invalid email or password")

    return render_template("login.html", form=form)


# --------------------
# LOGOUT
# --------------------
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# --------------------
# CREATE TICKET
# --------------------
@app.route("/create-ticket", methods=["GET", "POST"])
@login_required
def create_ticket():

    if request.method == "POST":

        import random

        ticket_code = f"HD-{random.randint(1000, 9999)}"

        ticket = Ticket(
            ticket_code=ticket_code,
            title=request.form.get("title"),
            description=request.form.get("description"),
            priority=request.form.get("priority"),
            user_id=current_user.id
        )

        db.session.add(ticket)
        db.session.commit()

        flash("Ticket created successfully")

        return redirect(url_for("home"))

    return render_template("create_ticket.html")


# --------------------
# RUN APP
# --------------------
if __name__ == "__main__":
    app.run(debug=True)