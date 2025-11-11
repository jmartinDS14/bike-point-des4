import json
import time
from datetime import datetime
import requests

#API documentation: https://api.tfl.gov.uk/swagger/ui/#!/BikePoint/BikePoint_GetAll
url = 'https://api.tfl.gov.uk/BikePoint'

def extract(url):
    
    response = requests.get(url,timeout=10)
    retry_codes = [429,500]

    count = 0
    max_tries = 3

    while count < max_tries:
        if response.status_code==200:
            #when API call successful, check the response is JSON
            try:
                data = response.json()
            except Exception as e:
                #if not print the error message and exit the while loop
                print(e)
                break

            extract_timestamp = datetime.now()
            for bp in data:
                #for each bikepoint in the data add in the extract timestamp as a key, value pair
                bp['extract_timestamp'] = str(extract_timestamp)

            #save the JSON file to the data folder
            filepath = 'data/' + extract_timestamp.strftime('%Y-%m-%dT%H-%M-%S') + '.json'
            with open(filepath,'w') as file:
                json.dump(data,file)
            break
        
        elif response.status_code in retry_codes:
            #if status code suggests issue on the server side, wait 20 seconds and retry
            time.sleep(20) 
            print(response.reason())
            count+=1
        
        else:
            #else there could be a user error, review code
            print(response.reason())
            break   
