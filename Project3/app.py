from flask import Flask, render_template

app = Flask(__name__)

visitors = []

@app.route("/")
@app.route("/welcome/")
def welcome():
	user = {"username": ""}
	return render_template("base.html",
							title="welcome",
							user=user,
							visitors=visitors)

@app.route("/app")
def to_do():
	return render_template("base_todo.html",
							title=f"{user} To Do List")

@app.route("/add", methods=["POST"])
def add():

if __name__ == "__main__":
	app.run()