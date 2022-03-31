# from crypt import methods
from atexit import register
from flask_app import app
from flask import render_template, redirect, request, session, flash


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# from flask_app.models.users import User
# from flask_app.models.tv_shows import TV_Show

@app.route("/login-register")
def login_register():
    return render_template("login-register.html")
    
#==============================================================
#register route
#==============================================================
#register route
@app.route("/register", methods = ["POST"])
def register_user():
    #collect data from the register form 
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"],       
        "email": request.form["email"]
    }
    #call upon validate user static method
    if not User.validate_user(data):
        return redirect("/")

    #bcrypt password
    print(request.form["password"])
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    #update the field of data object to be hashed password
    data["password"] = pw_hash
    # once user data is validated and password has been hashed, call upon register_user class method
    # passing in the data dictionary object, to run the query and register the user
    register = User.register_user(data)
    #enter user id into dashbboard and register user
    session["user_id"] = register
    return redirect("/dashboard")

#==============================================================
# #login route
#==============================================================
@app.route("/login", methods=["POST"])
def login():
    #collect data from the login form
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    #validate form data
    if not User.validate_login(data):
        return redirect("/")
    
    #login user

    logged_in_user = User.get_by_email(data)

    session["user_id"] = logged_in_user.id
    
    return redirect("/dashboard")

#=====================================
#dashboard / logged in route
#=====================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login/register before entering the site")
        return redirect("/")
    #set a data object user_id = the user_id set in session
    data = {
        "user_id" : session["user_id"]
    }
    #call upon get_user_by_id method passing in the data object with user_id from session,
    #to set it to the variable "data" to pass it along through index
    user = User.get_user_by_id(data)
    all_tv_shows = TV_Show.get_all()
    return render_template("dashboard.html", user = user, all_tv_shows = all_tv_shows)


#=====================================
#logout user route
#=====================================
@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out")
    return redirect("/")