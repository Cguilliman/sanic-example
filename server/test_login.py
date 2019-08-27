import requests
import json
from pprint import pprint


host = "http://127.0.0.1:9000/"
routers = {
    "login": host+"login/",
    "register": host+"register/",
    "room_create": host+"room/create/",
}


# response = requests.post(
#     routers["room_create"], 
#     data=json.dumps({
#         "user": "11"
#     }),
#     headers={
#         "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InVzZXJuYW1lNSJ9.AvGVG-KdVxoE5aunD7t5nvPxyDs9x3f2zZMhXk7MUVM"
#     }
# )


# 5(9) : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InVzZXJuYW1lNSJ9.AvGVG-KdVxoE5aunD7t5nvPxyDs9x3f2zZMhXk7MUVM
# 6(10) : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJ1c2VybmFtZTYifQ.RnXZH5kPIZlyL4I5KCr9b2Ua3eFFoqVdVadfEeGCW-U
# 7(11) : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMSwidXNlcm5hbWUiOiJ1c2VybmFtZTcifQ.VR3fOHcfj__i3Zk_yP2gnEI2aaEJClnkEWSOdBUQI-s


response = requests.post(
    routers['login'], 
    data=json.dumps({"username": "username5", "password": "username5"})
    # routers['register'], 
    # data=json.dumps({
    #     "username": "username7", 
    #     "password1": "username7", 
    #     "password2": "username7",
    # })
)


if response.status_code == 200:
    pprint(response.json())
else:
    print("fail")
