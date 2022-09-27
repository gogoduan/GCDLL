import requests
import json
from gallery.exceptions import logger

access_token1 = "24.2c7ffb3e4a6a7f425f1c89a2fc9d85d7"
access_token2 = ".2592000.1653531458.282335-26077203"
access_token = access_token1 + access_token2
"""
文本审核接口
"""
request_url1 = "https://aip.baidubce.com/rest/2.0/"
request_url2 = "solution/v1/text_censor/v2/user_defined"
request_url = request_url1 + request_url2


def is_legal(text):
    try:
        params = {"text": text}
        global request_url
        request_url = request_url + "?access_token=" + access_token
        headers = {"content-type": "application/x-www-form-urlencoded"}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            logger.info(response)
            if response.json().get("conclusion") == "合规":
                return True, "合规"
            else:
                return False, response.json().get("data")[0]["msg"]
        return False, "No response"
    except Exception:
        return True, "Error"
