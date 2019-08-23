import requests
import json
from pprint import pprint


host = "http://127.0.0.1:9000/"
routers = {
    "login": host+"login/",
    "register": host+"register/"
}


response = requests.post(
    # routers['register'], 
    routers['login'], 
    # data=json.dumps({"username": "username4", "password1": "username4", "password2": "username4"})
    data=json.dumps({"username": "username4", "password": "username4"})
)


if response.status_code == 200:
    pprint(response.json())
else:
    print("fail")



