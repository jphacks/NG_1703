# -*- coding:utf-8

import komagen_sd_client
from flask import Flask, render_template, abort
from flaski.models import WikiContent
import komagen_sd_client,py

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
	#komagen = komagen_sd_client.komagen()
	contents = WikiContent.query.all()
	return render_template("index.html", contents = contents)

if __name__ == "__main__":
	app.run()
