from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user_model import User
from forms.auth_forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login authentication route."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user_identifier = form.email.data.strip()
        password = form.password.data

        # Support login by Email, Username, OR Phone Number
        user = User.find_by_identifier(user_identifier)


        if user and user.check_password(password):
            if not user.is_active:
                flash("Your account has been deactivated. Please contact System Administrator.", "danger")
                return redirect(url_for('auth.login'))

            login_user(user)
            flash(f"Welcome back, {user.username}! Signed in as {user.role.upper()}.", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash("Invalid email/username or password. Please try again.", "danger")

    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Staff account creation route."""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data,
            phone=form.phone.data if form.phone.data else ''
        )

        if user:
            flash(f"User '{user.username}' created successfully as {user.role.upper()}!", "success")
            if not current_user.is_authenticated:
                login_user(user)
                return redirect(url_for('dashboard.index'))
            return redirect(url_for('auth.login'))
        else:
            flash("Failed to create account. Database error occurred.", "danger")

    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Sign out active user session."""
    logout_user()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile overview page."""
    return render_template('profile.html', user=current_user)
