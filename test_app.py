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
	url = "/remove/0"
	response = client.get(url)

	# make sure it redirects
	assert response.status_code == 302

	# make sure removed item not on home page
	response = client.get("/")
	webpage_text = response.get_data()
	assert b"Task 1" not in response.data

def check_afer(data, a, b):
	split_data = data.split(a)
	assert len(split_data) == 2, "String occured multiple times"
	return(b in split_data[1])

def test_up():
	# add an t3
	client = app.test_client()
	url = "/add/"
	data = {"new_todo": "Task 3"}
	response = client.post(url, data=data)	#add task 3

	data = {"new_todo": "Task 4"}
	response = client.post(url, data=data)	#add task 4

	#check task 3 comes after task 2
	response = client.get("/")
	webpage_text = response.get_data()
	assert check_afer(response.data, b"Task 2", b"Task 3")
	
	#check task 4 comes after task 3
	response = client.get("/")
	webpage_text = response.get_data()
	assert check_afer(response.data, b"Task 3", b"Task 4")
	#move task 3 up
	url = "/up/1"
	response = client.get(url)

	#move task 4 up
	url = "/up/2"
	response = client.get(url)

	#Check if 3 comes after 4
	response = client.get("/")
	webpage_text = response.get_data()
	assert check_afer(response.data, b"Task 3", b"Task 4")

	#Check if 2 comes after 4
	assert check_afer(response.data, b"Task 4", b"Task 2")


def test_down(): 
	pass

def test_toggle_check():
	pass

