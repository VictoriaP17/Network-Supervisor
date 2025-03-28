from flask import Blueprint, render_template, request


main_views = Blueprint("main_views", __name__)


@main_views.route("/", methods=["GET"])
def home():
    return render_template("index.html")