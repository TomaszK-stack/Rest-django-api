import requests

token = "Token fe0312ded6f8e497d1c764ae94716f13fedbe99e"

image_path = "C:\\Users\\korni\\HexOcean\\app\\static\\test_image"

with open(image_path + "\\test1.png", "rb") as image:
    files = {"image": image}
    response = requests.post("http://127.0.0.1:8000/api/v1/create/", data = files, headers={"Authorization": token })
    print(response)