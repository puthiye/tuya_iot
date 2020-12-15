import requests
import time
import datetime
import time as mod_time
from datetime import datetime
import hmac
import hashlib
import base64
import json

device_id = '00606071f4cfa2290ec3'
today = datetime.now()
today_time = int((mod_time.mktime(today.timetuple())))
today_unixtime = str((today_time*1000))

url_token = "https://openapi.tuyaus.com/v1.0/token?grant_type=1"
url_command = "https://openapi.tuyaus.com/v1.0/devices/" + device_id + "/commands"

#toggle the switch status 
payload="{\n\t\"commands\":[\n\t\t{\n\t\t\t\"code\": \"switch\",\n\t\t\t\"value\":false\n\t\t}\n\t]\n}"

#client_id, key = get this value from project - iot.tuya.com

headers_token = {
  'client_id': 'XXXXXXXXXXXXXXXX',
  'sign_method': 'HMAC-SHA256'
}


headers_command = {
  'client_id': 'XXXXXXXXXXXXXXXX',
  'sign_method': 'HMAC-SHA256',
  'Content-Type': 'application/json'
}

#secret
key = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

#form the access token parameters
#sign = hmac(key/secret, client_id + timestamp)
data_tok = headers_token['client_id'] + today_unixtime
sign_tok = hmac.new(key.encode('utf-8'), data_tok.encode('utf-8'), hashlib.sha256).hexdigest().upper()


headers_token['t'] = today_unixtime
headers_token['sign'] = sign_tok

#get access_token
response = requests.request("GET", url_token, headers=headers_token, data=payload)
resp_json = response.json()
print("Access token received....")
print(resp_json)


#form the command parameters
#sign = hmac(key/secret, client_id + access_token + timestamp)
data_cmd = headers_command['client_id'] + resp_json['result']['access_token'] + today_unixtime
sign_cmd = hmac.new(key.encode('utf-8'), data_cmd.encode('utf-8'), hashlib.sha256).hexdigest().upper()

headers_command['access_token'] = resp_json['result']['access_token']
headers_command['sign'] = sign_cmd
headers_command['t'] = today_unixtime

print("Sending command to device...")


#send command to device
response = requests.request("POST", url_command, headers=headers_command, data=payload)

print(response.text)
