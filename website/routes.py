from .app import app,mongo
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import url_for,render_template, request, redirect, session, flash, make_response,abort
from .models import hash_password ,User
from .emails import send_confirmation, send_password_change, confirm_token
import ast

users = mongo.db.users
login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.login_message_category ="danger"
login_manager.init_app(app)
from .routes_movies import *

@login_manager.user_loader
def load_user(id):
    id = ast.literal_eval(id)
    user = users.find_one({"email": id[0],"password":id[1]})
    if user:
        user = User(user)
    return user

@app.route('/login', methods=['POST'])
def signin_post():
    email = request.form['form_email']
    password = request.form['form_password']
    remember = request.form.get('form_remember') != None
    user = users.find_one({"email": email})
    if user:
        user = User(user)
        if(user.confirmed == False):
            flash('Check Your Email Please.', 'warning')
            send_confirmation(user.email)
            return redirect("/")
        elif user.password == hash_password(password , salt = user.salt)[0]:
            login_user(user, remember= remember)
            return redirect("/")
    
    flash('Invalid username or password.',category="danger")
    return redirect("/")



@app.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
        email = request.form['form_email']
        password = request.form['form_password']
        name = request.form['form_name']
        #validation here
        if users.find_one({"email": email}) == None:
            pw = hash_password(password)
            user = {"email":email,"password":pw[0],"name":name,"salt":pw[1],'confirmed_on':False,'confirmed': False,"movies":{}}
            users.insert_one(user)
            send_confirmation(email)
            flash('A confirmation email has been sent.',category="primary")
            return redirect("/")
        else:
            flash('Used Email.',category="danger")
            return render_template("register.html",data = name)  
    
    return render_template("register.html")


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['form_email']
        #validate
        user = users.find_one({'email':email})
        if user:
            send_password_change(email)
            flash('Email has been sent.',category="primary")
        else:
            flash('Invalid username or password.',category="danger")            
                
    return render_template("forgot_password.html")

@app.route('/change', methods=['POST'])
def change_password():
    password = request.form['form_password']
    try:
        email = request.cookies.get('email')
        print(email)
        token = request.cookies.get('token')
        print(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect("/forgot")
    #validate  
    if confirm_token(token,60*5) != False:
        pw = hash_password(password)
        users.update_one({ "email": email },{ "$set": {"password":pw[0],"salt":pw[1]} })
        resp = make_response(redirect("/"))
        resp.set_cookie('email', "",max_age=0) 
        resp.set_cookie('token', "",max_age=0) 
        flash('Password Changed!', 'success')
        return resp
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect("/forgot")
    

@app.route('/forgot/<token>')
def password_token(token):
    email = confirm_token(token,60*5)
    if email == False:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect("/forgot")
    else:
        resp = make_response(render_template('change_password.html'))
        resp.set_cookie('email', email,max_age=60*5) 
        resp.set_cookie('token', token,max_age=60*5) 
        return resp
    

@app.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if email == False:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect("/")
    user = users.find_one({"email": email})
    if user['confirmed']:
        flash('Account already confirmed. Please login.', 'success')
    else:
        users.update_one({ "email": email },{ "$set": { "confirmed": True } })
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect("/")

@app.route('/')
def index():
    if current_user.is_authenticated:
        if(current_user.confirmed):
            return render_template("index.html")
        else:
            flash('A confirmation email has been sent. ',category="primary")
    return render_template("login.html")
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out successfully.',category="primary")
    return redirect("/")


@app.route("/profile/", defaults={"token": None})
@app.route('/profile/<token>')
@login_required
def profile(token):
    if token == current_user.email:
        return redirect("/profile/")
    if not token:
        token = current_user.email
    user = users.find_one({"email": token})
    if user:
        user = User(user)
        return render_template("users_page.html",UserName = user.name,Image = "profile.png")
    else:
        return redirect("/")

    
    



    
