from flask import Blueprint, render_template, current_app, request, abort
from app.forms import LoginForm
import requests
import certifi
import ssl

bp = Blueprint("index_routes", __name__)


def verify_recaptcha(recaptcha_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": current_app.config["RECAPTCHA_PRIVATE_KEY"],
        "response": recaptcha_response,
    }
    response = requests.post(url, data=data)
    result = response.json()
    print(result["success"])
    print(result["score"])

    return result["success"] and result["score"] >= 0.5


@bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    username = None

    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            return abort(401)

    return render_template(
        "index.html",
        form=form,
        username=username,
        site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"],
    )
