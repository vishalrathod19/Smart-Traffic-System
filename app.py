from flask import Flask, render_template, Response, request, redirect, url_for, flash
from vehicle import counting_cars

# from detect import counting_cars
import flask_login

app = Flask(__name__)

app.secret_key = "super secret string"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {
    "root": {"password": "root"},
    "admin": {"password": "admin"},
    "test": {"password": "test"},
}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    if username not in users:
        return

    user = User()
    user.id = username
    return user




@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/technology")
def technology():
    return render_template("technology.html")


@app.route("/future-enhancements")
def future_enhancements():
    return render_template("future-enhancements.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form["username"]
    if username in users and request.form["password"] == users[username]["password"]:
        user = User()
        user.id = username
        flask_login.login_user(user)
        flash("Successfully signed in", "info")
        return redirect(url_for("demo"))

    flash("Invalid username or password", "danger")
    return redirect(url_for("signup"))


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("homepage"))


@app.route("/demo")
@flask_login.login_required
def demo():
    return render_template("demo.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        counting_cars(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True)
