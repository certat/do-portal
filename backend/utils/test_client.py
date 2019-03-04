import requests
from pprint import pprint

r = requests.get('http://localhost:8000/cp/1.0/ripe/contact/195.245.92.0%2F23',
     headers={
    'Accept': 'application/json',
    'API-Authorization': '1ae05c2103328c2955547ca1c6478cfe2d27e010d17fa5b7edb4b36a67c6108b'
     })

pprint(r)
