from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            host TEXT,
            time TEXT,
            table_name TEXT,
            children INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY date, time")
    orders = c.fetchall()
    conn.close()

    total_children = sum(order[5] for order in orders)
    salary = total_children * 30

    return render_template("index.html",
                           orders=orders,
                           total_children=total_children,
                           salary=salary)

@app.route("/add", methods=["POST"])
def add():
    data = (
        request.form["date"],
        request.form["host"],
        request.form["time"],
        request.form["table"],
        int(request.form["children"])
    )

    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("INSERT INTO orders (date, host, time, table_name, children) VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
