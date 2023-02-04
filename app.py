from flask import Flask,render_template,redirect,url_for,request
import sqlite3 as sql

app=Flask("__name__")

@app.route("/")
def Show():
    conn=sql.connect("students.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select * from stu")
    data=cur.fetchall()
    conn.close()
    return render_template("show.html",data=data)

@app.route("/insert",methods=["POST","GET"])
def Insert():
    if request.method=="POST":
        regno=request.form.get("regno")
        name=request.form["name"]
        email=request.form.get("email")

        conn=sql.connect("students.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("insert into stu (regno,name,email) values (?,?,?)",(regno,name,email))
        conn.commit()

        return redirect(url_for('Show'))
    
    return render_template("insert.html")

@app.route("/update/<id>",methods=["POST","GET"])
def Update(id):
    if request.method=="POST":
        regno=request.form.get("regno")
        name=request.form.get("name")
        email=request.form["email"]

        conn=sql.connect("students.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("update stu set name=?,email=? where regno=?",(name,email,regno))
        conn.commit()
        return redirect(url_for('Show'))
    conn=sql.connect("students.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select * from stu where regno=?",(id,))
    data=cur.fetchone()
    return render_template("update.html",data=data)

@app.route("/delete/<id>")
def Delete(id):
    conn=sql.connect("students.db")
    cur=conn.cursor()
    cur.execute("delete from stu where regno=?",(id,))
    conn.commit()
    return redirect(url_for("Show"))



if __name__=="__main__":
    app.run(debug=True)