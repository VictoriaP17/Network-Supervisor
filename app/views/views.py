from flask import Blueprint, render_template, request


main_views = Blueprint("main_views", __name__)


@main_views.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@main_views.route("/discovery", methods=["GET"])
def discovery_index():
    return render_template("discovery.html")


@main_views.route("/control_center/<device_id>", methods=["GET"])
def control_center_index(device_id):
    return render_template("device_console.html")