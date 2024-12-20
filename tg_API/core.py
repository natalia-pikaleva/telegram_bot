import requests

url = "https://booking-com18.p.rapidapi.com/web/stays/details"

querystring = {"id":"us/mayfair-new-york"}

headers = {
	"x-rapidapi-key": "ef6166b341msh19b1a0d737a25edp15588ejsna5729184331f",
	"x-rapidapi-host": "booking-com18.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.status_code)

print(response.json())