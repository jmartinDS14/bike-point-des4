from extract import extract
from load import load

url = 'https://api.tfl.gov.uk/BikePoint'

extract(url)
load()