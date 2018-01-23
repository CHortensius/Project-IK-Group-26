from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

import time

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

@app.route("/upload")
@login_required
def upload():
    if request.method == "POST":

        <?php
        $db = mysqli_connect("localhost", "root", "", "image_upload");

        $msg = "";

        if (isset($_POST['upload'])) {
  	        $image = $_FILES['image']['name'];
  	        $image_text = mysqli_real_escape_string($db, $_POST['image_text']);

  	        $target = "images/".basename($image);

  	        $sql = "INSERT INTO images (image, image_text) VALUES ('$image', '$image_text')";
  	        mysqli_query($db, $sql);

  	    if (move_uploaded_file($_FILES['image']['tmp_name'], $target)) {
  		    $msg = "Image uploaded successfully";
  	    }else{
  		    $msg = "Failed to upload image";
  	    }
    }
    $result = mysqli_query($db, "SELECT * FROM images");
?>

<!DOCTYPE html>
<html>
<head>
<title>Upload your masterpiece here!</title>
<style type="text/css">
   #content{
   	width: 50%;
   	margin: 20px auto;
   	border: 1px solid #cbcbcb;
   }
   form{
   	width: 50%;
   	margin: 20px auto;
   }
   form div{
   	margin-top: 5px;
   }
   #img_div{
   	width: 80%;
   	padding: 5px;
   	margin: 15px auto;
   	border: 1px solid #cbcbcb;
   }
   #img_div:after{
   	content: "";
   	display: block;
   	clear: both;
   }
   img{
   	float: left;
   	margin: 5px;
   	width: 300px;
   	height: 140px;
   }
</style>
</head>
<body>
<div id="content">


  <?php
    while ($row = mysqli_fetch_array($result)) {
      echo "<div id='img_div'>";
      	echo "<img src='images/".$row['image']."' >";
      	echo "<p>".$row['image_text']."</p>";
      echo "</div>";
    }
  ?>

  <form method="POST" action="index.php" enctype="multipart/form-data">
  	<input type="hidden" name="size" value="1000000">
  	<div>
  	  <input type="file" name="image">
  	</div>
  	<div>
      <textarea
      	id="text"
      	cols="40"
      	rows="4"
      	name="image_text"
      	placeholder="Say something about this image..."></textarea>
  	</div>
  	<div>
  		<button type="submit" name="upload">POST</button>
  	</div>
  </form>
</div>
</body>
</html>

    else:
        return render_template("newpass.html")


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
        if len(rows) != 1 or request.form.get("password") != rows[0]["hash"]:
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

    if request.method == "POST":

        # controleert of de gebruiker alle velden heeft ingevuld
        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("passwordconfirm"):
            return apology("must provide password confirmation")

        elif not request.form.get("email"):
            return apology("must provide e-mail adress")

        # controleert of de wachtwoorden matchen
        if request.form.get("password") != request.form.get("passwordconfirm"):
            return apology("passwords must match")

        # zet nieuwe gegevens in de database
        result = db.execute("INSERT INTO Accounts (username, hash, email) VALUES(:username, :pwdhash, :email)", username = request.form.get("username"), pwdhash = request.form.get("password"), email = request.form.get("email"))

        # geeft een error als de gebruikersnaam al bestaat
        if not result:
            return apology("username already exists")

        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/newpass", methods=["GET", "POST"])
@login_required
def newpass():
    """Laat de gebruiker zijn wachtwoord veranderen"""

    if request.method == "POST":

        # controleert of de gebruiker alle velden ingevuld heeft
        if not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("newpass"):
            return apology("must provide new password")

        elif not request.form.get("passwordconfirm"):
            return apology("must provide password confirmation")

        # controleert of de nieuwe wachtwoorden matchen
        if request.form.get("newpass") != request.form.get("passwordconfirm"):
            return apology("passwords must match")

        # haalt het huidige wachtwoord van de gebruiker erbij
        oldpass = db.execute("SELECT hash FROM users WHERE id = :id", id = session["user_id"])

        # controleert of de gebruiker het goede wachtwoord ingevuld heeft
        if not pwd_context.verify(request.form.get("password"), oldpass[0]["hash"]):
            return apology("invalid password")

        # update gebruiker's wachtwoord
        db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash = pwd_context.encrypt(request.form.get("newpass")), id = session["user_id"])

        # redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("newpass.html")

# Groetjes, Cas, Sooph en Lex