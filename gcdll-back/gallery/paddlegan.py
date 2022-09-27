import requests
import json
import base64
import re

with open("./static/avatar/1.jpeg", "rb") as f:
    img = f.read()

img_64 = base64.b64encode(img).decode("utf-8")


def paddle_fix(img_base64):
    api_key = "ca785101-e38e-4437-b454-13e3156b8809"
    request_url = "https://aistudio.baidu.com/serving/online/8951"
    params = {"image": img_base64}
    request_url = request_url + "?apiKey=" + api_key
    data = bytes(json.dumps(params), "utf8")
    response = requests.post(request_url, data=data, timeout=100)
    if response:
        try:
            img64 = response.json()["result"]["image"]
            img64 = re.sub("^data:image/.+;base64,", "", img64)
            img_data = base64.b64decode(img64)
            with open("./static/photo/processed/paddle_fixed.jpeg", "wb") as f:
                f.write(img_data)
        except:
            print(response.json())


paddle_fix(img_64)
