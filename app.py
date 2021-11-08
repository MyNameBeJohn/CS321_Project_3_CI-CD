from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

todo_list = []


@app.route("/")
def home():
    return render_template("base.html", enumerated_todo_list=enumerate(todo_list))

@app.route("/add/", methods=["POST"])
def add():
	new_todo_item = request.form.get("new_todo")
	todo_list.append((new_todo_item, {"check":0}))

	return redirect(url_for("home"))


@app.route("/remove/<int:task_number>")
def remove(task_number):
	todo_list.pop(task_number)
	return redirect(url_for("home"))


@app.route("/up/<int:task_number>")
def up(task_number):
	if task_number != 0: 
		todo_list[task_number-1], todo_list[task_number] = todo_list[task_number], todo_list[task_number-1]

	return redirect(url_for("home"))	


@app.route("/down/<int:task_number>")
def down(task_number):
	if task_number != len(todo_list)-1: 
		todo_list[task_number], todo_list[task_number+1] = todo_list[task_number+1], todo_list[task_number]

	return redirect(url_for("home"))	

@app.route("/toggle_check/<int:task_number>")
def toggle_check(task_number): 
	todo_list[task_number][1]["check"] = 0 if todo_list[task_number][1]["check"] else 1

	return redirect(url_for("home"))	


if __name__ == "__main__":
	app.run()