from flask import render_template, url_for, flash, redirect, Blueprint, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_paginate import get_page_args
from project import db
from project.models import User, BlogPost
from project.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from project.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__, template_folder='templates/users')

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User (email= form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registration", "success")
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET','POST'])
def login():
   
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully', 'success')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
        else:
            flash("Email and/0r password not correct", 'danger')
            return redirect('login.html')
        return redirect(next or url_for('users.account'))
    return render_template('login.html',form=form)


# @users.route('/account/<str:username>', methods=['GET','POST'])
@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)



@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.created_on.desc()).paginate(page=page,per_page =5)
#    blog_posts = BlogPost.query.filter_by(user_id=)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)