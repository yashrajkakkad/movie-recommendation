import requests

response = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=aa03d634')
print(response.status_code)
print(response.content)