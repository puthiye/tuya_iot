import requests
import time
import datetime
import time as mod_time
from datetime import datetime
import hmac
import hashlib
import base64

today = datetime.now()
today_time = int((mod_time.mktime(today.timetuple())))
today_unixtime = str((today_time*1000))

url = "https://openapi.tuyaus.com/v1.0/token?grant_type=1"

payload={}

#client_id, key = get this value from project - iot.tuya.com

headers = {
  'client_id': 'XXXXXXXXXXXXXXXXXXXXX',
  'sign_method': 'HMAC-SHA256'
}

key = 'XXXXXXXXXXXXXXXXXXXXX'
data = headers['client_id'] + today_unixtime
sign = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest().upper()

headers['t'] = today_unixtime
headers['sign'] = sign


#get access_token
response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
