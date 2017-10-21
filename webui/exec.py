# -*- coding:utf-8

from flask import Flask, render_template, abort
from flaski.models import WikiContent

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
	contents = WikiContent.query.all()
	return render_template("index.html", contents=contents)

if __name__ == "__main__":
	app.run()
