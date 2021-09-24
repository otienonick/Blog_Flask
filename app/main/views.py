from flask import render_template
from . import main
from ..requests import get_quote



@main.route("/")
def home():
    quotes = get_quote()
    return render_template("index.html",  quotes=quotes)
