from flask import Flask, render_template, url_for, request
import psycopg2, random

db = psycopg2.connect("dbname='notes' user='username' password='password'")
ix = db.cursor()

letters = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz"

ix.execute("CREATE TABLE IF NOT EXISTS notes(id VARCHAR, note VARCHAR);")
db.commit()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    if request.method == "GET":
        return render_template("index.html", page="")
    else:
        text = request.form.get('textarea')
        if text != "" and text != " ":
            while True:
                key = ""
                for i in range(0, 4): key+=letters[random.randint(0, 57)]
                ix.execute("SELECT * FROM notes WHERE id='{0}'".format(key))
                if ix.fetchone() == None: break
            turp = (key, text)
            ix.execute("INSERT INTO notes(id, note) VALUES (%s, %s)", turp)
            db.commit()
            return render_template("index2.html", note=text, code=key)
        
@app.route("/<code>")
def appIndex(code):
    ix.execute("SELECT note FROM notes WHERE id='{0}'".format(code))
    value = ix.fetchone()
    if value == None: text = "The note is not available!"
    else: text = value[0]
    return render_template("index.html", page=text)
        

if __name__ == "__main__": app.run(debug = True)