from flask import Flask, render_template, url_for
#import pandas as pd

app = Flask(__name__)

#@app.route("/")
#def home():
#    return "/"


@app.route("/Hello_World")
def hello():
    return "Hello World!"


@app.route("/page_1")
def page_1():
    my_f = open('example_1.txt')
    lines = my_f.read()
    my_f.close()

    text = { 'info': lines }
    return render_template("page_1.html",
                           title = "list",
                           text = text)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
@app.route("/main")
def parental():
    return render_template("main.html")



if __name__ == "__main__":
    app.run(debug=True)

