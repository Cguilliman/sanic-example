import requests
import json
from pprint import pprint


host = "http://127.0.0.1:9000/"
routers = {
    "login": host+"login/",
    "register": host+"register/"
}


response = requests.post(
    routers['register'], 
    # routers['login'], 
    data=json.dumps({
        "username": "username5", 
        "password1": "username5", 
        "password2": "username5",
    })
    # data=json.dumps({"username": "username4", "password": "username4"})
)


if response.status_code == 200:
    pprint(response.json())
else:
    print("fail")
