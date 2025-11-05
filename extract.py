import json
import time
from datetime import datetime
import requests

url = 'https://api.tfl.gov.uk/BikePoint'

response = requests.get(url,timeout=10)

data = response.json()

extract_timestamp = datetime.now()

for bp in data:
    bp['extract_timestamp'] = str(extract_timestamp)

filepath = 'data/' + extract_timestamp.strftime('%Y-%m-%dT%H-%M-%S') + '.json'

with open(filepath,'w') as file:
    json.dump(data,file)