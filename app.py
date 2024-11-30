from flask import Flask, render_template


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
