from flask_app import app, bcrypt
from flask_app.models import usermodel
from flask import render_template,redirect,request,session,flash

@app.route('/')
def index():
    if "logged_in_id" not in session:
        return redirect('/welcome')
    else:
        user_id = session["logged_in_id"]
        return redirect(f"/user/{user_id}")

@app.route('/welcome')
def landing():
    return render_template('index.html')

@app.route('/newuser', methods = ['POST'])
def register():
    one_user = usermodel.User.get_user_by_email(request.form)
    if one_user:
        flash("Invalid email", 'reg')
        return redirect('/welcome')
    if not usermodel.User.new_user(request.form):
        return redirect('/welcome')
    usermodel.User.create_new_user(request.form)
    flash("Account created succesfully", 'reg')
    return redirect('/welcome')

@app.route('/login', methods = ['GET','POST'])
def login():
    one_user = usermodel.User.get_user_by_email(request.form)
    if not one_user:
        flash("Invalid email", 'login')
        return redirect('/welcome')
    if not bcrypt.check_password_hash(one_user.password,(request.form["password"])):
        flash("Incorrect password", 'login')
        return redirect('/welcome')
    session['logged_in_id'] = one_user.id
    return redirect(f"/user/{one_user.id}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/welcome')

@app.route('/user/<int:id>')
def user_card(id):
    if 'logged_in_id' not in session:
        flash("Please sign in", 'login')
        return redirect('/welcome')
    data = {
        'id' : id
    }
    one_user = usermodel.User.get_user_by_id(data)
    if not one_user.id == session['logged_in_id']: 
        flash("You are not authorized", 'user')
        return redirect("/")
    print(one_user)
    return render_template('user_card.html', user = one_user)

