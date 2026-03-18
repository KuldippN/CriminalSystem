from flask import Flask, render_template, request, redirect, session, flash ,url_for
import sqlite3
import os                                     # ← new import
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename   # ← new import

app = Flask(__name__)
app.secret_key = "secret123"

# directory where uploaded photos will be saved
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/add_criminal", methods=["GET","POST"])
def add_criminal():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        crime = request.form["crime"]

        image = request.files.get("image")

        filename = ""

        if image and image.filename != "":
            filename = image.filename
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = sqlite3.connect("criminals.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO criminals (name,age,crime,image) VALUES (?,?,?,?)",
            (name, age, crime, filename)
        )

        conn.commit()
        conn.close()

        flash("Criminal record added successfully", "success")
        return redirect(url_for('dashboard'))          # ← goes to /dashboard
    
    # GET request
    return render_template("add_criminal.html")


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = sqlite3.connect('criminals.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS criminals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            crime TEXT,
            image TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user"] = user["username"]
        return redirect("/dashboard")

    flash("Invalid username or password")
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")


@app.route("/records")
def records():

    conn = sqlite3.connect("criminals.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM criminals")
    criminals = cursor.fetchall()

    conn.close()

    return render_template("records.html", criminals=criminals)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)