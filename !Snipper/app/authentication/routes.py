from app.authentication import authentication_bp
from flask import render_template, flash, redirect, request, url_for
from app.authentication.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse

@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    # In case already logged-in user accidentally navigates to /login
    if current_user.is_authenticated:
        return redirect(url_for('dailybriefing.dailybriefing'))
    form = LoginForm()

    # If form is submitted, check db if user info is correct then flash error or log user in
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('authentication.login'))
        login_user(user, remember=form.remember_me.data)
        
        # Navigate to page user requested before login was required, or dailybriefing 
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dailybriefing.dailybriefing')
        return redirect(next_page)
    
    # Display login page - previous block is skipped when page first loads
    return render_template('login.html', title='Login', form=form)


@authentication_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))