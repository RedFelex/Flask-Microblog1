from flask import render_template, flash, redirect, url_for, request
from app import new_app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@new_app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@new_app.route('/')
@new_app.route('/index')
@login_required
def index():

    posts = [
        {'author': {'userName': 'Elena'},
         'body': {'post number 1'}
         },
        {'author': {'userName': 'Susan'},
         'body': {'post number 2'}
         }
    ]
    return render_template('index.html', title = 'Home',  posts = posts)



@new_app.route('/login', methods = ['POST','GET'])
def login():

    if current_user.is_authenticated:
        return  redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me = {}'.format(form.userName.data, form.remember_me.data))

        user = User.query.filter_by(userName=form.userName.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid UserName or Password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            return redirect(url_for('index'))
        return redirect(next_page)

    return render_template('login.html', title = 'Sign in', form = form)



@new_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@new_app.route('/register', methods = ['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(userName=form.userName.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you fre now a register user!')
        return  redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@new_app.route('/user/<userName>')
@login_required
def user(userName):
    user = User.query.filter_by(userName = userName).first_or_404()

    posts = [{'author': user, 'body':'Test post #1'},
             {'author': user, 'body': 'Test post #2'}
             ]
    return render_template('user.html', user=user, posts=posts)



@new_app.route('/edit_profile', methods = ['POST','GET'])
@login_required
def edit_profile():

    form = EditProfileForm(current_user.userName)

    if form.validate_on_submit():
        current_user.userName = form.userName.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))

    elif request.method =='GET':
        form.userName.data = current_user.userName
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile', form=form)
