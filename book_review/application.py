import os

from flask import Flask, session,render_template,request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests


#goodreads api key
KEY = "fT5VgEzJ34Vm3eArcFlLyQ"

app = Flask(__name__)

# Check for environment variable
#heroku database use by adminer.cs50.net
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "GET":
        if session.get("login") is None:
            session["login"] = 0
            return render_template("notlog.html")
        elif session["login"] == 0:
            return render_template("notlog.html")
        else:
            return render_template("logged.html", name = session["name"])
    else:
        return redirect("/")

@app.route("/register", methods=["POST","GET"] )
def register():
    if request.method == "GET":
        return render_template("register.html", message = "Try to use unique username", login = 0)
    else:
        name = request.form.get("username")
        password = request.form.get("password")
        if db.execute("select * from username where name=:name",{"name": name}).rowcount != 0:
            return render_template("register.html", message = "username is used", login = 0)
        elif password == None:
            return render_template("register.html", message = "at least put some effort in password", login = 0)
        else:
            db.execute("insert into username(name, password) values (:name,:password)",{"name":name,"password":password})
            session["login"] = 1
            session["name"] = name
            db.commit()
            return redirect("/")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("register.html", message = "enter your username", login = 1)
    else:
        name = request.form.get("username")
        password = request.form.get("password")
        if db.execute("select * from username where name=:name and password = :password",{"name": name,"password":password}).rowcount == 0:
            return render_template("register.html", message = "username/password is incorrect", login = 1)
        else:
            session["login"] = 1
            session["name"] = name
            return redirect("/")


@app.route("/logout")
def logout():
    session["login"] = 0
    session["name"] = ""
    return redirect("/")



@app.route("/search", methods =["GET","POST"])
def search():
    if request.method == "GET":
        if session['login'] == 0:
            return redirect("/")
        return render_template("search.html",searched = 0)
    else:
        bookdetail = request.form.get("bookdetail")
        count = db.execute(f"select title,isbn,author from books where isbn like '%{bookdetail}%' or author like '%{bookdetail}%' or title like '%{bookdetail}%'").rowcount
        data = db.execute(f"select title,isbn,author from books where isbn like '%{bookdetail}%' or author like '%{bookdetail}%' or title like '%{bookdetail}%'").fetchall()
        return render_template("search.html", searched = 1, count = count, data=data)


@app.route("/<string:isbn>", methods=["GET","POST"])
def bookpage(isbn):
    if request.method == "GET":
        if session['login'] == 0:
            return redirect("/")
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn})
        if res.status_code == 200:
            bookread = res.json()
            ratingscount = bookread['books'][0]["ratings_count"]
            averagerating = bookread['books'][0]["average_rating"]
        else:
            ratingscount = "not available"
            averagerating = "notavailable"
        data = db.execute("select * from books where isbn = :isbn",{"isbn":isbn}).fetchall()
        _userdata = db.execute("select * from review where isbn = :isbn and name = :name",{"isbn":isbn, "name":session["name"]}).fetchall()
        userdatarow = db.execute("select * from review where isbn = :isbn and name = :name",{"isbn":isbn, "name":session["name"]}).rowcount
        publicdata = db.execute("select * from review where isbn = :isbn",{"isbn":isbn}).fetchall()
        reviewcount = db.execute("select * from review where isbn = :isbn",{"isbn":isbn}).rowcount
        if len(data) == 0:
            return redirect("/search")
        row = data[0]
        if userdatarow == 0:
            return render_template("bookpage.html", review = 1, publicdata = publicdata, reviewcount = reviewcount,row=row, ratingscount=ratingscount,averagerating=averagerating)
        userdata = _userdata[0]
        return render_template("bookpage.html", review = 0, publicdata = publicdata, reviewcount = reviewcount, userdata = userdata,row=row, ratingscount=ratingscount,averagerating=averagerating)
    else:
        rating = request.form.get("rating")
        review = request.form.get("review")
        db.execute("insert into review(isbn,name,star,review) values(:isbn,:name,:star,:review)",{"isbn":isbn,"name":session["name"],"star":rating,"review":review})
        db.commit()
        return redirect(f"/{isbn}")



@app.route("/api/<string:isbn>")
def api(isbn):
    _data = db.execute("select * from books where isbn = :isbn",{"isbn":isbn}).fetchall()
    count = db.execute("select * from books where isbn = :isbn",{"isbn":isbn}).rowcount
    if count == 0:
        return jsonify({"error":"the given Isbn is not in our record"}),404
    data = _data[0]
    _review_count = db.execute("select count(*) from review where isbn = :isbn",{"isbn":isbn}).fetchall()
    review_count = _review_count[0]
    _average_rating = db.execute("select avg(star) from review where isbn = :isbn",{"isbn":isbn}).fetchall()
    average_rating = _average_rating[0]
    return jsonify({"title":data.title,"author":data.author,"year":data.year,"isbn":data.isbn,"review_count": review_count["count"],"average_score": str(round(average_rating["avg"],2))})
