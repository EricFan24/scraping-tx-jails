import requests 
from bs4 import BeautifulSoup 
from pprint import pprint

response = requests.get("https://www.tdcj.texas.gov/death_row/dr_offenders_on_dr.html")
html = response.content

soup = BeautifulSoup(html)
table = soup.find("table")

final = []
for row in table.findAll("tr"):
	this_row = []
	for cell in row.findAll("td"):
		this_row.append(cell.text)
	final.append(this_row)

pprint(final)

