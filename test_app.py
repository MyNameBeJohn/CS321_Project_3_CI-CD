from app import *
import requests


website_path = "https://to-do-cs321.herokuapp.com/"
#website_path = "http://127.0.0.1:5000/"

def test_welcome():
	# more intreesting way to test the the page works
	client = app.test_client()
	response = client.get("/welcome")
	assert response.status_code == 200  # success