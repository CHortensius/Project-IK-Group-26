from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from imgurpython import ImgurClient

from helpers import *
from secret import *

import shutil
import time
import os

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///accounts.db")

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/imagepagina/<clickedpic>/<clickeduser>", methods=["GET" , "POST"])
def imagepagina(clickedpic, clickeduser):

    clickedpic = int(clickedpic)

    photo = db.execute("SELECT url, comment, userid FROM pics WHERE picid = :id", id = clickedpic)

    users = db.execute("SELECT username, id FROM Accounts")
    user = ""
    for user in users:
        if clickeduser == user["id"]:
            userlist[clickeduser] = str(user["username"])



    return render_template('imagepagina.html', photo=photo, username = user, clickedpic = clickedpic)

@app.route("/gebruikerspagina/<clickeduser>/<clickedname>", methods=["GET" , "POST"])
def gebruikerspagina(clickeduser, clickedname):

    clickeduser = int(clickeduser)

    photoprofile = db.execute("SELECT url, comment, picid FROM pics WHERE userid = :id", id = clickeduser)

    #username = users[clickeduser-1]["username"]

    for photo in photoprofile:
        eindfoto = photo["url"]
        eindcomment = photo["comment"]
        eindid = eindcomment = photo["picid"]
    return render_template('gebruikerspagina.html', photoprofile=photoprofile, username = clickedname, clickeduser = clickeduser)

@app.route("/discover", methods=["GET", "POST"])
def discover():
    photoprofile = db.execute("SELECT url, comment, picid, userid FROM pics ")
    users = db.execute("SELECT username, id FROM Accounts")
    userlist = {}
    for profile in photoprofile:
        for user in users:
            if profile["userid"] == user["id"]:
                userlist[profile["userid"]] = user["username"]

    for photo in photoprofile:
        eindfoto = photo["url"]
        eindcomment = photo["comment"]
        eindid = eindcomment = photo["picid"]
    return render_template('discover.html', photoprofile=photoprofile, userlist = userlist)

@app.route("/profielpagina", methods=["GET" , "POST"])
@login_required
def profielpagina():

    userid = session["user_id"]
    photoprofile = db.execute("SELECT url, comment FROM pics WHERE userid = :id", id = userid)
    #comments = db.execute("SELECT comment FROM pics WHERE userid = :id", id = session["user_id"])
    for photo in photoprofile:
        eindfoto = photo["url"]
        eindcomment = photo["comment"]
    return render_template('profielpagina.html', photoprofile=photoprofile, user = userid)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        UPLOAD_FOLDER = os.path.abspath("ImgurApi/")
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        file = request.files["image"]
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
        file.save(f)
        client_id= '978480f212b2fba'
        client_secret= secret_code
        refresh_token= '80ddfe566ccfc68403b632be352fa4c7bb53ad0e'
        access_token= 'f8abdffaf2902a85d6ebb44af4f4d2c010d095bd'

        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        image = client.upload_from_path(f, anon=True)


        db.execute("INSERT INTO pics (userid, url, comment) VALUES(:userid, :url, :comment)", userid=session["user_id"], url=image['link'], comment=request.form.get("comment"))

        return redirect(url_for("profielpagina"))

    else:
        return render_template("upload.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM Accounts WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("discover"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must provide username")

        elif not request.form.get("password"):
            return apology("Must provide password")

        elif not request.form.get("passwordconfirm"):
            return apology("Must provide Check password")

        elif request.form.get("password") != request.form.get("passwordconfirm"):
            return apology("Password doesn't match!")

        password = request.form.get("password")
        hash = pwd_context.encrypt(password)

        result = db.execute("INSERT INTO Accounts (username,hash) VALUES (:username, :hash)", \
            username=request.form.get("username"), hash=hash)

        if not result:
            return apology("Username already in use")

        session["user_id"] = result

        return redirect(url_for("discover"))

    else:
        return render_template("register.html")




# Groetjes, Cas, Sooph en Lex