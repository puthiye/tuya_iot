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

#client_id, key = get this value from project - iot.tuya.com
headers_token = {
  'client_id': 'ckjwhruaa5nsvfwbjltf',
  'sign_method': 'HMAC-SHA256'
}


headers_command = {
  'client_id': 'ckjwhruaa5nsvfwbjltf',
  'sign_method': 'HMAC-SHA256',
  'Content-Type': 'application/json'
}

#secret
key = '366106568dbf4d79bb9aa4a146c60280'

def send_command(method, url_command, payload):

  #form the access token parameters
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
  data_cmd = headers_command['client_id'] + resp_json['result']['access_token'] + today_unixtime
  sign_cmd = hmac.new(key.encode('utf-8'), data_cmd.encode('utf-8'), hashlib.sha256).hexdigest().upper()

  headers_command['access_token'] = resp_json['result']['access_token']
  headers_command['sign'] = sign_cmd
  headers_command['t'] = today_unixtime

  print("Sending command to device...")


  #send command to device
  response = requests.request(method, url_command, headers=headers_command, data=payload)

  print(response.text)


method = "POST"
url_command = "https://openapi.tuyaus.com/v1.0/devices/" + device_id + "/commands"
#set countdown time
payload="{\n\t\"commands\":[\n\t\t{\n\t\t\t\"code\": \"countdown_1\",\n\t\t\t\"value\":120\n\t\t}\n\t]\n}"
send_command(method, url_command, payload)
