from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


class LoginForm(FlaskForm):
    name = StringField(
        "Name", validators=[Length(5, 10, "Need to be between 5 and 10")]
    )
    age = IntegerField("Age")
    sex = StringField("Sex")
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
