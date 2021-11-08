from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

todo_list = []


@app.route("/")
def home():
    return render_template("base.html", todo_list=todo_list)

@app.route("/add/", methods=["POST"])
def add():
	new_todo_item = request.form.get("new_todo")
	todo_list.append(new_todo_item)

	return redirect(url_for("home"))


@app.route("/remove/<string:task>")
def remove(task):
	todo_list.remove(task)
	return redirect(url_for("home"))


if __name__ == "__main__":
	app.run()