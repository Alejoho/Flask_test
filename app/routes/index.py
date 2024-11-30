from flask import Blueprint, render_template
from app.forms import LoginForm

bp = Blueprint("index_routes", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()

    return render_template("index.html", form=form)
