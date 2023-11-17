from initial_scripts import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user,current_user
from initial_scripts.models import User
from initial_scripts.forms import LoginForm, RegistrationForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # User already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully!')

            next_page = request.args.get('next')

            if next_page is None or not next_page[0] == '/':
                next_page = url_for('welcome_user')
            return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
