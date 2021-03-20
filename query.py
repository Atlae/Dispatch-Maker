import requests
from bs4 import BeautifulSoup

version = 3.0
print("Version No. %.1f" % version)

# if you want more flexibility, you can use the custom query
bidsTrue = False
nation = input("What nation are you collecting from? ").lower().replace(" ", "_")
season = 3
while season not in [1, 2]:
    season = input("What season are you looking for? (1 or 2) ")
    try:
        season = int(season)
    except ValueError:
        print("That's not a number!")
    except season == 3:
        print("S3 will never come.")
custom = input("Do you want to make your own custom query? (yes/no) ").lower().startswith('y')
if not custom:
	region = input("What region are you searching? ").lower().replace(" ", "_")
	bids = input("Are you looking for the cards to bid on? (yes/no) ")
	if bids.lower().startswith('y'):
		bidsTrue = True

if custom:
	posted_query = input("Please enter your query using the Advanced Cards Queries syntax: ")
	processed_query = posted_query.replace(":", "%3A").replace("&", "%26").replace("!", "%21").replace("|", "%7C").replace(" ", "+").replace("(", "%28").replace(")", "%29")
	query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query={processed_query}&season={season}&format=full&submit=submit'
elif bidsTrue:
	query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query=region%3A{region}%26%21deck%3A{nation}%26%21bid%3A{nation}&season={season}&format=full&submit=submit'
else:
	query = f'http://azure.nsr3n.info/card_queries/get_daemon_advanced.sh?format=full&query=region%3A{region}%26%21deck%3A{nation}&season={season}&format=full&submit=submit'

print('Running...accessing r3n\'s server')
reqs = requests.get(query)
soup = BeautifulSoup(reqs.text, 'html.parser')
print("Finished accessing r3n\'s server")

print("Writing the output of said query into file")
with open('query_links.txt', 'w') as f:
	a = soup.find_all('a')
	for i in range(1, len(a)-1):
		f.write(a[i].get('href') + '\n')
	f.write(a[len(a)-1].get('href'))

links = open('query_links.txt', 'r')
cards = open('cards.txt', 'w')
for link in links:
	link = link.replace("https://www.nationstates.net/page=deck/card=", "")
	link = link.replace("/season=", " ")
	cards.write(link)
