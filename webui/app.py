# -*- coding:utf-8

import komagen_sd_client
from flask import Flask, render_template, abort
from flaski.models import WikiContent
import komates

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
	contents = WikiContent.query.all()
	return render_template("index.html", contents = contents)

@app.route("/", methods=["POST"])
def callkomagen():
	koma = komates.komagen()
	return koma

if __name__ == "__main__":
	app.run()
