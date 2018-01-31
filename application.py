from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from imgurpython import ImgurClient
from passlib.hash import sha256_crypt
import urllib.request,json
from urllib.parse import urljoin

from helpers import *
from secret import *

import shutil
import time
import os
import secret
import requests

from PIL import Image

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

    if session.get("user_id") is not None:
        return redirect(url_for('friends'))

    return redirect(url_for('discover'))

@app.route("/imagepagina/<clickedpic>/<clickeduser>", methods=["GET" , "POST"])
def imagepagina(clickedpic, clickeduser):

    clickedpic = int(clickedpic)

    likecheck = False

    if session.get("user_id") is not None:
        result = db.execute("SELECT * FROM likes WHERE user_id = :user_id AND like_id = :like_id", user_id = session["user_id"], like_id = clickedpic )
        if result != []:
            likecheck = True

    photo = db.execute("SELECT * FROM pics WHERE picid = :id", id = clickedpic)

    users = db.execute("SELECT username, id FROM Accounts")
    user = ""
    for user in users:
        if clickeduser == user["id"]:
            userlist[clickeduser] = str(user["username"])

    comments = db.execute("SELECT * FROM comments WHERE picid= :picid", picid = clickedpic)

    return render_template('imagepagina.html', photo=photo, username = user, clickedpic = clickedpic, clickeduser = clickeduser, comments = comments, likecheck = likecheck)

@app.route("/follow/<clickeduser>/<clickedname>", methods=["GET" , "POST"])
@login_required
def follow(clickeduser,clickedname):
    result = db.execute("SELECT * FROM follow WHERE user_id = :userid AND following_id = :following_id", userid = session["user_id"], following_id = clickeduser )
    if result == []:
        followcheck = False
    else:
        followcheck = True

    ###############
    if followcheck == False:
        db.execute("INSERT INTO follow(user_id,following_id) VALUES(:user_id,:following_id)",user_id=session["user_id"],following_id=clickeduser)
    elif followcheck == True:
        db.execute("DELETE FROM follow WHERE user_id = :user_id AND following_id = :following_id",user_id = session["user_id"],following_id = clickeduser)

    return redirect(url_for('gebruikerspagina',clickeduser=clickeduser,clickedname = clickedname))

@app.route("/like/<clickeduser>/<clickedpic>", methods=["GET" , "POST"])
@login_required
def like(clickeduser, clickedpic):
    result = db.execute("SELECT * FROM likes WHERE user_id = :user_id AND like_id = :like_id", user_id = session["user_id"], like_id = clickedpic )

    if result == []:
        likecheck = False
    else:
        likecheck = True

    if likecheck == False:
        db.execute("INSERT INTO likes(user_id, like_id) VALUES(:user_id,:like_id)", user_id=session["user_id"], like_id=clickedpic)
    elif likecheck == True:
        db.execute("DELETE FROM likes WHERE user_id = :user_id AND like_id = :like_id",user_id = session["user_id"],like_id = clickedpic)

    return redirect(url_for('imagepagina',clickeduser=clickeduser,clickedpic = clickedpic))

@app.route("/gebruikerspagina/<clickeduser>/<clickedname>", methods=["GET" , "POST"])
def gebruikerspagina(clickeduser, clickedname):

    clickeduser = int(clickeduser)

    if session.get("user_id") is not None:
        if session["user_id"] == clickeduser:
            return redirect(url_for("profielpagina"))

    photoprofile = db.execute("SELECT * FROM pics WHERE userid = :id ORDER BY picid DESC", id = clickeduser)

    userinfo = db.execute("SELECT * FROM Accounts WHERE id = :id", id = clickeduser)

    followcheck = False

    if session.get("user_id") is not None:
        result = db.execute("SELECT * FROM follow WHERE user_id = :userid AND following_id = :followingid", userid = session["user_id"], followingid = clickeduser)
        if result != []:
            followcheck = True


    for photo in photoprofile:
        eindfoto = photo["url"]
        eindcomment = photo["comment"]
        eindid = eindcomment = photo["picid"]
    return render_template('gebruikerspagina.html', photoprofile=photoprofile, username = clickedname, clickeduser = clickeduser,followcheck = followcheck, userinfo = userinfo)

@app.route("/discover", methods=["GET", "POST"])
def discover():
    photoprofile = db.execute("SELECT * FROM pics ORDER BY picid DESC")
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

@app.route("/friends", methods=["GET", "POST"])
@login_required
def friendspagina():

    volgend = db.execute("SELECT following_id from follow WHERE user_id = :userid", userid=session["user_id"])
    volgerslijst = []
    for volgers in volgend:
        volgerslijst.append(volgers["following_id"])
    print(volgerslijst)

    photoprofile = db.execute("SELECT * FROM pics WHERE userid IN (:volgerslijst) ORDER BY picid DESC ", volgerslijst=volgerslijst)
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
    return render_template('friends.html', photoprofile=photoprofile, userlist = userlist)

@app.route("/profielpagina", methods=["GET" , "POST"])
@login_required
def profielpagina():

    userid = session["user_id"]
    photoprofile = db.execute("SELECT * FROM pics WHERE userid = :id ORDER BY picid DESC", id = userid)
    #comments = db.execute("SELECT comment FROM pics WHERE userid = :id", id = session["user_id"])
    for photo in photoprofile:
        eindfoto = photo["url"]
        eindcomment = photo["comment"]

    userinfo = db.execute("SELECT * FROM Accounts WHERE id = :id", id = userid)

    return render_template('profielpagina.html', photoprofile=photoprofile, user = userid, userinfo = userinfo)

@app.route("/postcomment/<clickedpic>/<clickeduser>", methods=["GET", "POST"])
@login_required
def postcomment(clickedpic, clickeduser):
    if not request.form.get("title"):
        return apology("must provide subject")
    if not request.form.get("comment"):
        return apology("must enter comment")

    db.execute("INSERT INTO comments (userid, picid, comment, poscomment, negcomment, title) VALUES(:userid, :picid, :comment, :poscomment, :negcomment, :title)", userid = session["user_id"], picid = clickedpic, comment = request.form.get("comment"), poscomment = request.form.get("poscomment"), negcomment = request.form.get("negcomment"), title = request.form.get("title") )

    return redirect(url_for('imagepagina', clickedpic = clickedpic , clickeduser = clickeduser))

@app.route("/profilegif", methods=["GET" , "POST"])
@login_required
def profilegif():
    if request.method == "POST":

        if not request.form.get("gifsearch"):
            return apology("must provide search value")

        hoofd_url = "http://api.giphy.com/v1/gifs/search?q="
        public_key = "&api_key=dc6zaTOxFJmzC&limit=1"
        search_value = request.form.get("gifsearch")
        joined_url = hoofd_url + search_value + public_key

        data = json.loads(requests.get(joined_url).text)
        gif_url = json.dumps(data["data"][0]["images"]["original"]["url"]).strip('"')

        db.execute("UPDATE Accounts SET profilegif = :profilegif WHERE id = :id", profilegif = gif_url, id = session["user_id"])

        return render_template('profilegif.html', gif_url = gif_url)


    else:
        return render_template("profilegif.html")

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if not request.form.get("title"):
            return apology("must provide title")

        if not request.form.get("comment"):
            return apology("must provide description")


        UPLOAD_FOLDER = os.path.abspath("ImgurApi/")
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        file = request.files["image"]

        #if not file:
            #return apology("I don't see an image here...")
        #try:
            #im=Image.open(file)
        #except IOError:
            #return apology("That's not an image!")

        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(f)
        client_id= '978480f212b2fba'
        client_secret= secret_code
        refresh_token= '80ddfe566ccfc68403b632be352fa4c7bb53ad0e'
        access_token= 'f8abdffaf2902a85d6ebb44af4f4d2c010d095bd'

        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        image = client.upload_from_path(f,anon=True)

        db.execute("INSERT INTO pics (userid, url, comment, title) VALUES(:userid, :url, :comment, :title)", userid=session["user_id"], url=image['link'], comment=request.form.get("comment"), title=request.form.get("title"))
        picid = db.execute("SELECT picid FROM pics WHERE url = :url", url = image["link"])

        return redirect(url_for('imagepagina', clickedpic = picid[0]["picid"] , clickeduser = session["user_id"]))

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
        if len(rows) != 1 or not sha256_crypt.verify(request.form.get("password"), rows[0]["hash"]):
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
        hash = sha256_crypt.hash(password)

        result = db.execute("INSERT INTO Accounts (username,hash) VALUES (:username, :hash)", \
            username=request.form.get("username"), hash=hash)

        if not result:
            return apology("Username already in use")

        session["user_id"] = result

        return redirect(url_for("discover"))

    else:
        return render_template("register.html")

@app.route("/about", methods=["GET" , "POST"])
def about():
     return render_template("about.html")




# Groetjes, Cas, Sooph en Lex