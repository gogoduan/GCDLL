# encoding:utf-8
import requests

apikey = "1DYySKrkUt6sp43bVfYH4fN9"
secrete_key = "SKhR0rTTeEoLFV6QtxucWCw6Ol4mmUBc"
# client_id Ϊ������ȡ��AK�� client_secret Ϊ������ȡ��SK
host = "https://aip.baidubce.com/oauth/2.0/\
token?grant_type=client_credentials&client_id={}&client_secret={}".format(
    apikey, secrete_key
)
response = requests.get(host)
if response:
    print(response.json())
