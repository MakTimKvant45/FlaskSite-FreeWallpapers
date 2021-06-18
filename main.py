from sqlite3.dbapi2 import Cursor
from typing import SupportsRound
from flask import Flask, render_template, flash, wrappers
from flask import redirect
from flask import request
from hashlib import sha256
from flask import session
from flask.helpers import url_for
import os
import sqlite3
import os.path

app = Flask(__name__)
app.secret_key = b'asdasjosdfusyhgydrtyuerdyl'

@app.route('/')
def index():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC LIMIT 11")
    papers = papers.fetchall()

    user = None
    if "user" in session:
        user = session["user"]

    return render_template('index.html', user=user, papers=papers)

@app.route('/nature')
def nature():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]

    return render_template('nature.html', user=user,  papers=papers)

@app.route('/anime')
def anime():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('anime.html',  papers=papers, user=user)

@app.route('/animals')
def animals():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('animals.html',  papers=papers, user=user)

@app.route('/auto')
def auto():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('auto.html',  papers=papers, user=user)

@app.route('/game')
def game():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('game.html',  papers=papers, user=user)

@app.route('/future')
def future():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('future.html',  papers=papers, user=user)

@app.route('/pixel')
def pixel():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('pixel.html',  papers=papers, user=user)

@app.route('/minimalism')
def minimalism():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('minimalism.html', user=user, papers=papers)

@app.route('/space')
def space():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('space.html',  papers=papers, user=user)

@app.route('/meme')
def meme():
    conn = sqlite3.connect("WPapers.db")
    c = conn.cursor()
    papers = c.execute("SELECT * FROM Papers ORDER BY id DESC")
    papers = papers.fetchall()
    user = None
    if "user" in session:
        user = session["user"]
    return render_template('meme.html',  papers=papers, user=user)

@app.route('/search', methods=["GET", "POST"])
def search():
    con = sqlite3.connect("WPapers.db")
    cursor = con.cursor()
    search = None
    search = request.form["search"]
    if search != None:
        cursor.execute(f"SELECT * FROM Papers WHERE title LIKE '%{search}%' OR content LIKE '%{search}%'")
    else:
        cursor.execute("SELECT * FROM Papers")
    WPapers = cursor.fetchall()
    
    user = None
    if "user" in session:
        user = session["user"]
    return render_template("search.html", WPapers=WPapers, user=user)             

@app.route("/reg")
def reg():
    return render_template("reg.html")
@app.route("/logout")
def logout():
    session.clear()
    session["user"] = None
    return redirect(url_for('index'))


@app.route("/fun/reg", methods=["POST"])
def fun_reg():
    username = request.form["login"]
    password = request.form["password"]
    hashPassword = sha256( request.form["password"].encode("utf-8") ).hexdigest()
    email = request.form["email"]
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    return redirect("/")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/fun/login", methods=["POST"])
def fun_login():
    r = ""
    username = request.form["login"]
    password = request.form["password"]
    hashPassword = sha256( request.form["password"].encode("utf-8") ).hexdigest()
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = '"+username+"' AND password = '"+password+"' ")
    r = c.fetchall()
    for i in r:
        if (username == i[1] and password == i[2]):
            session["user"] = username
            return redirect("/")
        else:
            return redirect("/login")

@app.route("/create")
def create():
    user = None
    if "user" in session:
        user = session["user"]
    return render_template("create.html", user=user)

@app.route("/fun/create", methods=["POST"])
def fun_create():
    
    title = request.form["title"]
    content = request.form["content"]
    kategory = request.form["kategory"]

    file = request.files["photo"]
    
    if kategory != "Категория" and title != "" and file != "":
        file.save(os.path.join("static/upload", file.filename))

        con = sqlite3.connect("WPapers.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO Papers (title, content, kategory, filename) VALUES (?, ?, ?, ?)", (title, content, kategory, file.filename))      
        con.commit()
        return redirect("/")
    else:
        return redirect("/create")

if __name__ == "__main__":
    app.run()