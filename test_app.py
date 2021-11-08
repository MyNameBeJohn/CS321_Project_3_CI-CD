from app import *
from flask import template_rendered

# website_path = "https://to-do-cs321.herokuapp.com/"
website_path = "http://127.0.0.1:5000/"

def test_home():
	# more intreesting way to test the the page works
	client = app.test_client()
	response = client.get("/")
	print(response.status_code)
	assert response.status_code == 200  # success


def test_add():
	# add an item
	client = app.test_client()
	url = "/add/"
	data = {"new_todo": "Task 1"}
	response = client.post(url, data=data)

	# make sure it redirects
	assert response.status_code == 302

	# make sure item is on home page
	response = client.get("/")
	webpage_text = response.get_data()
	assert b"Task 1" in response.data

	# add another item
	data = {"new_todo": "Task 2"}
	response = client.post(url, data=data)

	# check list len
	assert len(todo_list) == 2

	# make sure both added items on home page
	response = client.get("/")
	webpage_text = response.get_data()
	assert b"Task 1" in response.data
	assert b"Task 2" in response.data


def test_remove():
	client = app.test_client()

	# make sure item is on home page
	response = client.get("/")
	webpage_text = response.get_data()
	assert b"Task 1" in response.data

	# remove item
	url = "/remove/Task 1"
	response = client.get(url)

	# make sure it redirects
	assert response.status_code == 302

	# make sure removed item not on home page
	response = client.get("/")
	webpage_text = response.get_data()
	print(webpage_text)
	assert b"Task 1" not in response.data

