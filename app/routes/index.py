from flask import Blueprint, render_template, current_app, url_for
from email.mime.text import MIMEText
from app.forms import LoginForm
import smtplib
import os

bp = Blueprint("index_routes", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    username = None

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        form.username.data = ""
        form.email.data = ""

        activation_email = create_activation_email(email)
        send_email(email, activation_email)
        token = activation_email.as_string()

    return render_template("index.html", form=form, username=username)


def generate_activation_link(recipient):
    serializer = current_app.config["SERIALIZER"]
    token = serializer.dumps(recipient, "email_confirmation")
    link = f"127.0.0.1:5000{url_for("index_routes.confirm_email", token=token)}"
    return link


def create_activation_email(recipient):
    link = generate_activation_link(recipient)

    message_body = f"Please follow this link to activate your account:\n{link}"

    message = MIMEText(message_body)
    message["From"] = os.getenv("GMAIL_ACCOUNT")
    message["To"] = recipient
    message["Subject"] = "Account Activation"

    return message


def send_email(recipient, email):
    with smtplib.SMTP(
        current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"]
    ) as email_server:
        print("server ready")

        email_server.starttls()
        print("server started")

        email_server.login(
            current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"]
        )
        print("server logged")

        email_server.sendmail(
            current_app.config["MAIL_USERNAME"], recipient, email.as_string()
        )
        print("email sent")


@bp.get("/confirm_email/<token>")
def confirm_email(token):
    serializer = current_app.config["SERIALIZER"]

    try:
        email = serializer.loads(token, salt="email_confirmation", max_age=60)
    except:
        return "Something went wrong with the confirmation try again"

    return "The email works"
