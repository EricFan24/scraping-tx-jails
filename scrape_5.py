import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.tdcj.texas.gov/death_row/dr_offenders_on_dr.html")
html = response.content

soup = BeautifulSoup(html)
table = soup.find("table")

for row in table.findAll("tr"):
	for cell in row.findAll("td"):
		print(cell.text)


