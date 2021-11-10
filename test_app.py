from app import *
from flask import template_rendered
from datetime import datetime

# website_path = "https://to-do-cs321.herokuapp.com/"
website_path = "http://127.0.0.1:5000/"


def test_home():
    # more intreesting way to test the the page works
    client = app.test_client()
    response = client.get("/")
    print(response.status_code)
    assert response.status_code == 200  # success


def test_add():
    # Get Current Time:
    current_time = datetime.now().strftime("%H:%M")

    # add an item
    client = app.test_client()
    url = "/add/"
    data = {
        "new_todo": "Task 1",
        "priority": "3",
        "dow": "Tuesday",
        "tags": "Home Dog",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)

    # make sure it redirects
    assert response.status_code == 302

    # make sure item is on home page
    response = client.get("/")
    webpage_text = response.get_data()
    assert b"Task 1" in response.data

    assert len(todo_list[1]) == 1
    assert todo_list[1][0][0] == "Task 1"
    assert todo_list[1][0][1]["check"] == 0
    assert todo_list[1][0][1]["priority"] == "3"
    assert todo_list[1][0][1]["tags"] == ["#Home", "#Dog"]
    assert todo_list[1][0][1]["time"] == current_time

    # Get current time again
    current_time = datetime.now().strftime("%H:%M")

    # add another item
    data = {
        "new_todo": "Task 2",
        "priority": "2",
        "dow": "Tuesday",
        "tags": "Yard",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)

    # check list len
    assert len(todo_list[1]) == 2
    assert todo_list[1][1][0] == "Task 2"
    assert todo_list[1][1][1]["check"] == 0
    assert todo_list[1][1][1]["priority"] == "2"
    assert todo_list[1][1][1]["tags"] == ["#Yard"]
    assert todo_list[1][1][1]["time"] == current_time

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
    url = "/remove/1/0"
    response = client.get(url)

    # make sure it redirects
    assert response.status_code == 302

    # make sure removed item not on home page
    response = client.get("/")
    webpage_text = response.get_data()
    assert b"Task 1" not in response.data
    assert todo_list[1][0][0] == "Task 2"


def test_up():
    def check_afer(data, a, b):
        split_data = data.split(a)
        assert len(split_data) == 2, "String occured multiple times"
        return b in split_data[1]

    # add an t3
    client = app.test_client()
    url = "/add/"
    data = {
        "new_todo": "Task 3",
        "priority": "2",
        "dow": "Tuesday",
        "tags": "Yard",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)  # add task 3

    data = {
        "new_todo": "Task 4",
        "priority": "2",
        "dow": "Tuesday",
        "tags": "Yard",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)  # add task 4

    assert todo_list[1][0][0] == "Task 2"
    assert todo_list[1][1][0] == "Task 3"
    assert todo_list[1][2][0] == "Task 4"

    # check task 3 comes after task 2
    response = client.get("/")
    webpage_text = response.get_data()
    assert check_afer(response.data, b"Task 2", b"Task 3")

    # check task 4 comes after task 3
    response = client.get("/")
    webpage_text = response.get_data()
    assert check_afer(response.data, b"Task 3", b"Task 4")

    # move task 3 up
    url = "/up/1/1"
    response = client.get(url)

    assert todo_list[1][0][0] == "Task 3"
    assert todo_list[1][1][0] == "Task 2"
    assert todo_list[1][2][0] == "Task 4"

    # move task 4 up
    url = "/up/1/2"
    response = client.get(url)

    assert todo_list[1][0][0] == "Task 3"
    assert todo_list[1][1][0] == "Task 4"
    assert todo_list[1][2][0] == "Task 2"

    # Check if 4 comes after 3
    response = client.get("/")
    webpage_text = response.get_data()
    assert check_afer(response.data, b"Task 3", b"Task 4")

    # Check if 2 comes after 4
    assert check_afer(response.data, b"Task 4", b"Task 2")

    # ensure moving top item doesnt break anything
    url = "/up/1/0"
    response = client.get(url)

    assert todo_list[1][0][0] == "Task 3"
    assert todo_list[1][1][0] == "Task 4"
    assert todo_list[1][2][0] == "Task 2"

    # ensure 4 still comes after 3
    response = client.get("/")
    webpage_text = response.get_data()
    assert check_afer(response.data, b"Task 3", b"Task 4")

    # ensure 2 still comes after 4
    assert check_afer(response.data, b"Task 4", b"Task 2")


def test_down():
    client = app.test_client()
    url = "/down/1/0"
    response = client.get(url)

    assert todo_list[1][0][0] == "Task 4"
    assert todo_list[1][1][0] == "Task 3"
    assert todo_list[1][2][0] == "Task 2"

    url = "/down/1/1"
    response = client.get(url)

    assert todo_list[1][0][0] == "Task 4"
    assert todo_list[1][1][0] == "Task 2"
    assert todo_list[1][2][0] == "Task 3"

    # test putting lowest item down, nothing should change
    url = "/down/1/2"
    response = client.get(url)

    assert todo_list[1][0][0] == "Task 4"
    assert todo_list[1][1][0] == "Task 2"
    assert todo_list[1][2][0] == "Task 3"

    url = "/down/1/0"
    response = client.get(url)

    assert todo_list[1][0][0] == "Task 2"
    assert todo_list[1][1][0] == "Task 4"
    assert todo_list[1][2][0] == "Task 3"


def test_toggle_check():
    client = app.test_client()

    assert todo_list[1][0][1]["check"] == 0

    url = "/toggle_check/1/0"
    response = client.get(url)

    assert todo_list[1][0][1]["check"] == 1

    url = "/toggle_check/1/0"
    response = client.get(url)

    assert todo_list[1][0][1]["check"] == 0

    assert todo_list[1][1][1]["check"] == 0

    url = "/toggle_check/1/1"
    response = client.get(url)

    assert todo_list[1][1][1]["check"] == 1

    url = "/toggle_check/1/1"
    response = client.get(url)

    assert todo_list[1][1][1]["check"] == 0


def test_archive():
    client = app.test_client()

    assert len(todo_list[1]) == 3

    url = "/clear"
    response = client.get(url)

    assert len(todo_list[1]) == 3

    url = "/toggle_check/1/1"
    response = client.get(url)
    url = "/toggle_check/1/2"
    response = client.get(url)

    url = "/clear"
    response = client.get(url)

    assert len(todo_list[1]) == 1
    assert len(archived) == 2

    url = "/add/"
    data = {
        "new_todo": "Task 1",
        "priority": "1",
        "dow": "Friday",
        "tags": "Yard",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)
    data = {
        "new_todo": "Task 2",
        "priority": "2",
        "dow": "Wednesday",
        "tags": "Yard",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)
    data = {
        "new_todo": "Task 3",
        "priority": "3",
        "dow": "Monday",
        "tags": "Yard",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)
    data = {
        "new_todo": "Task 4",
        "priority": "4",
        "dow": "Sunday",
        "tags": "Yard",
        "time": datetime.now().strftime("%H:%M"),
    }
    response = client.post(url, data=data)

    url = "/toggle_check/0/0"
    response = client.get(url)
    url = "/toggle_check/1/0"
    response = client.get(url)
    url = "/toggle_check/2/0"
    response = client.get(url)
    url = "/toggle_check/4/0"
    response = client.get(url)
    url = "/toggle_check/6/0"
    response = client.get(url)

    url = "/clear"
    response = client.get(url)

    assert len(todo_list[0]) == 0
    assert len(todo_list[1]) == 0
    assert len(todo_list[2]) == 0
    assert len(todo_list[4]) == 0
    assert len(todo_list[6]) == 0

    assert len(archived) == 7
