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

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///accounts.db")

@app.route("/")
def index():
    # Brengt gebruiker naar zijn feed als hij is ingelogd, anders naar de discoverpagina
    if session.get("user_id") is not None:
        return redirect(url_for('friendspagina'))

    return redirect(url_for('discover'))

@app.route("/imagepagina/<clickedpic>/<clickeduser>", methods=["GET" , "POST"])
def imagepagina(clickedpic, clickeduser):

    clickedpic = int(clickedpic)
    clickeduser = int(clickeduser)

    likecheck = False

    result = []

    # Controleert of de gebruiker deze foto geliked heeft
    if session.get("user_id") is not None:
        result = checkforlike(clickedpic)
        if result != []:
            likecheck = True

    likecount = len(likecounts(clickedpic))

    photo = showphoto(clickedpic)

    # Maakt een dictionary met welke username bij een id hoort
    userlist = makeuserlist()

    username = userlist[clickeduser]

    comments = showcomment(clickedpic)

    return render_template('imagepagina.html',likecount = likecount ,photo=photo, username = username, clickedpic = clickedpic, clickeduser = clickeduser, comments = comments, likecheck = likecheck, userlist = userlist)

@app.route("/follow/<clickeduser>/<clickedname>", methods=["GET" , "POST"])
@login_required
def follow(clickeduser,clickedname):

    # Controleert of de gebruiker dit account al volgt of niet
    result = checkforfollow(clickeduser)
    if result == []:
        followcheck = False
    else:
        followcheck = True

    # Volgt of onvolgt dit account
    if followcheck == False:
        addfollower(clickeduser)
    elif followcheck == True:
        deletefollower(clickeduser)

    return redirect(url_for('gebruikerspagina',clickeduser=clickeduser,clickedname = clickedname))

@app.route("/like/<clickeduser>/<clickedpic>", methods=["GET" , "POST"])
@login_required
def like(clickeduser, clickedpic):
    # Controleert of de gebruiker deze foto al geliked heeft
    result = checkforlike(clickedpic)
    if result == []:
        likecheck = False
    else:
        likecheck = True

    # Liket of onliket de foto
    if likecheck == False:
        addlike(clickedpic)
    elif likecheck == True:
        deletelike(clickedpic)

    return redirect(url_for('imagepagina',clickeduser=clickeduser,clickedpic = clickedpic))

@app.route("/gebruikerspagina/<clickeduser>/<clickedname>", methods=["GET" , "POST"])
def gebruikerspagina(clickeduser, clickedname):

    clickeduser = int(clickeduser)

    # Gaat naar de profielpagina als dit de gebruiker zijn eigen pagina is
    if session.get("user_id") is not None:
        if session["user_id"] == clickeduser:
            return redirect(url_for("profielpagina"))

    photoprofile = showphotogebruiker(clickeduser)

    userinfo = getuserinfo(clickeduser)

    followcheck = False

    followcount = len(countfollowers(clickeduser))

    # Controleert of de gebruiker dit account volgt
    if session.get("user_id") is not None:
        result = checkforfollowers(clickeduser)
        if result != []:
            followcheck = True

    showmultiplephotos(photoprofile)
    return render_template('gebruikerspagina.html', followcount = followcount, photoprofile=photoprofile, username = clickedname, clickeduser = clickeduser,followcheck = followcheck, userinfo = userinfo)

@app.route("/discover", methods=["GET", "POST"])
def discover():
    photoprofile = showphotosdiscover()
    users = selectusers()
    userlist = makeuserlist()

    showmultiplephotos(photoprofile)
    return render_template('discover.html', photoprofile=photoprofile, userlist = userlist)

@app.route("/friends", methods=["GET", "POST"])
@login_required
def friendspagina():
    # Kijkt welke accounts de gebruiker volgt
    volgend = userfollows()
    volgerslijst = []
    for volgers in volgend:
        volgerslijst.append(volgers["following_id"])

    anyfollowing = False
    #Controleert of de gebruiker minstens 1 accounts volgt
    if volgend != []:
        anyfollowing = True

    photoprofile = showphotosfriends(volgerslijst)
    users = selectusers()
    userlist = makeuserlist()

    showmultiplephotos(photoprofile)
    return render_template('friends.html', photoprofile=photoprofile, userlist = userlist, anyfollowing = anyfollowing)

@app.route("/profielpagina", methods=["GET" , "POST"])
@login_required
def profielpagina():
    # Kijkt welke foto's de gebruiker heeft gepost
    photoprofile = showphotosprofile()
    for photo in photoprofile:
        eindfoto = photo["url"]
        eindcomment = photo["comment"]

    followcount = len(countfollowersprofile())

    userinfo = getmyinfo()

    return render_template('profielpagina.html',followcount = followcount, photoprofile=photoprofile, userinfo = userinfo)

@app.route("/postcomment/<clickedpic>/<clickeduser>", methods=["GET", "POST"])
@login_required
def postcomment(clickedpic, clickeduser):
    # Controleert of de gebruiker alle benodigde velden heeft ingevuld
    if not request.form.get("title"):
        return apology("must provide subject")
    if not request.form.get("comment"):
        return apology("must enter comment")

    showcommentfromuser(clickedpic)

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

        # Laat de gebruiker het eerste zoekresultaat zien
        data = json.loads(requests.get(joined_url).text)
        gif_url = json.dumps(data["data"][0]["images"]["original"]["url"]).strip('"')
        # Zet deze gif als de gebruiker's profielfoto
        updateprofilegif(gif_url)

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

        # definieert de uploadfolder
        UPLOAD_FOLDER = os.path.abspath("ImgurApi/")
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        file = request.files["image"]

        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Slaat de geuploade foto op
        file.save(f)
        client_id= '978480f212b2fba'
        client_secret= secret_code
        refresh_token= '80ddfe566ccfc68403b632be352fa4c7bb53ad0e'
        access_token= 'f8abdffaf2902a85d6ebb44af4f4d2c010d095bd'

        # Gebruikt de imgurPython plugin om de foto naar imgur te uploaden
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        image = client.upload_from_path(f,anon=True)
        image_url = image["link"]
        uploadphoto(image_url)
        picid = selectpicid(image_url)

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
        rows = usernamecheck()

        # ensure username exists and password is correct
        if len(rows) != 1 or not sha256_crypt.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

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
        # Encrypt het wachtwoord
        hash = sha256_crypt.hash(password)

        result = createaccount(hash)

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