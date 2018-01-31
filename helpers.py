import csv
import urllib.request
from cs50 import SQL

from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///accounts.db")

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def checkforlike(clickedpic):
    return db.execute("SELECT * FROM likes WHERE user_id = :user_id AND like_id = :like_id", user_id = session["user_id"], like_id = clickedpic )

def likecounts(clickedpic):
    return db.execute("SELECT * FROM likes WHERE like_id = :like_id",like_id = clickedpic)

def showphoto(clickedpic):
    return db.execute("SELECT * FROM pics WHERE picid = :id", id = clickedpic)

def makeuserlist():
    userlist = {}
    users = db.execute("SELECT username, id FROM Accounts")
    for user in users:
            userlist[user["id"]] = str(user["username"])
    return userlist

def showcomment(clickedpic):
    return db.execute("SELECT * FROM comments WHERE picid= :picid", picid = clickedpic)

def checkforfollow(clickeduser):
    return db.execute("SELECT * FROM follow WHERE user_id = :userid AND following_id = :following_id", userid = session["user_id"], following_id = clickeduser )

def addfollower(clickeduser):
    return db.execute("INSERT INTO follow(user_id,following_id) VALUES(:user_id,:following_id)",user_id=session["user_id"],following_id=clickeduser)

def deletefollower(clickeduser):
    return db.execute("DELETE FROM follow WHERE user_id = :user_id AND following_id = :following_id",user_id = session["user_id"],following_id = clickeduser)

def checkforlike(clickedpic):
    return db.execute("SELECT * FROM likes WHERE user_id = :user_id AND like_id = :like_id", user_id = session["user_id"], like_id = clickedpic )

def addlike(clickedpic):
    return db.execute("INSERT INTO likes(user_id, like_id) VALUES(:user_id,:like_id)", user_id=session["user_id"], like_id=clickedpic)

def deletelike(clickedpic):
    return db.execute("DELETE FROM likes WHERE user_id = :user_id AND like_id = :like_id",user_id = session["user_id"],like_id = clickedpic)

def showphotogebruiker(clickeduser):
    return db.execute("SELECT * FROM pics WHERE userid = :id ORDER BY picid DESC", id = clickeduser)

def getuserinfo(clickeduser):
    return db.execute("SELECT * FROM Accounts WHERE id = :id", id = clickeduser)

def countfollowers(clickeduser):
    return db.execute("SELECT * FROM follow WHERE following_id = :followingid",followingid = clickeduser)

def checkforfollowers(clickeduser):
    return db.execute("SELECT * FROM follow WHERE user_id = :userid AND following_id = :followingid", userid = session["user_id"], followingid = clickeduser)

def showmultiplephotos(photoprofile):
    for photo in photoprofile:
        eindfoto = photo["url"]
        eindcomment = photo["comment"]
        eindid = eindcomment = photo["picid"]

def showphotosdiscover():
    return db.execute("SELECT * FROM pics ORDER BY picid DESC")

def selectusers():
    return db.execute("SELECT username, id FROM Accounts")

def userfollows():
    return db.execute("SELECT following_id from follow WHERE user_id = :userid", userid=session["user_id"])

def showphotosfriends(volgerslijst):
    return db.execute("SELECT * FROM pics WHERE userid IN (:volgerslijst) ORDER BY picid DESC ", volgerslijst=volgerslijst)

def showphotosprofile():
    return db.execute("SELECT * FROM pics WHERE userid = :id ORDER BY picid DESC", id = session["user_id"])

def countfollowersprofile():
    return db.execute("SELECT * FROM follow WHERE following_id = :followingid",followingid = session["user_id"])

def getmyinfo():
    return db.execute("SELECT * FROM Accounts WHERE id = :id", id = session["user_id"])

def showcommentfromuser(clickedpic):
    return db.execute("INSERT INTO comments (userid, picid, comment, poscomment, negcomment, title) VALUES(:userid, :picid, :comment, :poscomment, :negcomment, :title)", userid = session["user_id"], picid = clickedpic, comment = request.form.get("comment"), poscomment = request.form.get("poscomment"), negcomment = request.form.get("negcomment"), title = request.form.get("title") )

def updateprofilegif(gif_url):
    return db.execute("UPDATE Accounts SET profilegif = :profilegif WHERE id = :id", profilegif = gif_url, id = session["user_id"])

def uploadphoto(image_url):
    return db.execute("INSERT INTO pics (userid, url, comment, title) VALUES(:userid, :url, :comment, :title)", userid=session["user_id"], url=image_url, comment=request.form.get("comment"), title=request.form.get("title"))

def selectpicid(image_url):
    return db.execute("SELECT picid FROM pics WHERE url = :url", url = image_url)

def usernamecheck():
    return db.execute("SELECT * FROM Accounts WHERE username = :username", username=request.form.get("username"))

def createaccount(hash):
    return db.execute("INSERT INTO Accounts (username,hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hash)










