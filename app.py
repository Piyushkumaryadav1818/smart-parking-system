from flask import Flask,render_template,request,redirect,session
import sqlite3
import qrcode

app = Flask(__name__)
app.secret_key="parking_secret"

# DATABASE CONNECT
def connect_db():
    return sqlite3.connect("parking.db")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        db=connect_db()
        db.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,p))
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        db=connect_db()
        user=db.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p)).fetchone()
        db.close()

        if user:
            session["user"]=u
            return redirect("/slots")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

# ---------------- SLOTS PAGE ----------------
@app.route("/slots")
def slots():
    db=connect_db()
    slots=db.execute("SELECT * FROM slots").fetchall()
    free=db.execute("SELECT COUNT(*) FROM slots WHERE status='Free'").fetchone()[0]
    occ=db.execute("SELECT COUNT(*) FROM slots WHERE status='Occupied'").fetchone()[0]
    db.close()
    return render_template("slots.html",slots=slots,free=free,occ=occ)

# ---------------- PAYMENT PAGE ----------------
@app.route("/pay/<slot>")
def pay(slot):
    return render_template("payment.html",slot=slot)

# ---------------- PAYMENT SUCCESS ----------------
@app.route("/success/<slot>")
def success(slot):
    return render_template("success.html",slot=slot)

# ---------------- BOOK SLOT + QR ----------------
@app.route("/book/<slot>")
def book(slot):
    user=session["user"]

    db=connect_db()
    db.execute("UPDATE slots SET status='Occupied' WHERE slot=?",(slot,))
    db.execute("INSERT INTO bookings(username,slot) VALUES(?,?)",(user,slot))
    db.commit()
    db.close()

    # QR GENERATE
    data=f"User:{user} Slot:{slot}"
    img=qrcode.make(data)
    img.save("static/booking_qr.png")

    return render_template("ticket.html",slot=slot)

# ---------------- CANCEL BOOKING ----------------
@app.route("/cancel/<slot>")
def cancel(slot):
    db=connect_db()
    db.execute("UPDATE slots SET status='Free' WHERE slot=?",(slot,))
    db.execute("DELETE FROM bookings WHERE slot=?",(slot,))
    db.commit()
    db.close()
    return redirect("/slots")

# ---------------- MY BOOKING ----------------
@app.route("/mybooking")
def mybooking():
    user=session["user"]
    db=connect_db()
    data=db.execute("SELECT * FROM bookings WHERE username=?",(user,)).fetchall()
    db.close()
    return render_template("mybooking.html",data=data)

# ---------------- BOOKING HISTORY ----------------
@app.route("/history")
def history():
    user=session["user"]
    db=connect_db()
    data=db.execute("SELECT * FROM bookings WHERE username=?",(user,)).fetchall()
    db.close()
    return render_template("history.html",data=data)

# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin():
    db=connect_db()
    data=db.execute("SELECT * FROM bookings").fetchall()
    db.close()
    return render_template("admin.html",data=data)

# ---------------- ADMIN RESET ----------------
@app.route("/reset")
def reset():
    db=connect_db()
    db.execute("UPDATE slots SET status='Free'")
    db.execute("DELETE FROM bookings")
    db.commit()
    db.close()
    return redirect("/admin")

# ---------------- RUN ----------------
    if __name__ == "__main__":
    app.run()