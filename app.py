from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("businesses.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS businesses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category TEXT,
                    location TEXT,
                    rating INTEGER,
                    approved INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

init_db()

# --- HOME PAGE ---
@app.route("/")
def index():
    conn = sqlite3.connect("businesses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM businesses WHERE approved=1")
    businesses = c.fetchall()
    conn.close()
    return render_template("index.html", businesses=businesses)

# --- ADD BUSINESS ---
@app.route("/add", methods=["GET", "POST"])
def add_business():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        location = request.form["location"]
        rating = request.form["rating"]

        conn = sqlite3.connect("businesses.db")
        c = conn.cursor()
        c.execute("INSERT INTO businesses (name, category, location, rating) VALUES (?, ?, ?, ?)",
                  (name, category, location, rating))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_business.html")

# --- ADMIN PAGE ---
@app.route("/admin")
def admin():
    conn = sqlite3.connect("businesses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM businesses")
    businesses = c.fetchall()
    conn.close()
    return render_template("admin.html", businesses=businesses)

# --- APPROVE BUSINESS ---
@app.route("/approve/<int:business_id>")
def approve(business_id):
    conn = sqlite3.connect("businesses.db")
    c = conn.cursor()
    c.execute("UPDATE businesses SET approved=1 WHERE id=?", (business_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

# --- DELETE BUSINESS ---
@app.route("/delete/<int:business_id>")
def delete(business_id):
    conn = sqlite3.connect("businesses.db")
    c = conn.cursor()
    c.execute("DELETE FROM businesses WHERE id=?", (business_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)
