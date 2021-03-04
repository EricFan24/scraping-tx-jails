import requests 
from bs4 import BeautifulSoup 
import csv

response = requests.get("https://www.tdcj.texas.gov/death_row/dr_offenders_on_dr.html")
html = response.content

soup = BeautifulSoup(html)
table = soup.find("table")

final = []
for row in table.findAll("tr")[2:]:
    this_row = []
    for cell in row.findAll("td"):
        if cell.a: # if we're a link tag
            this_row.append("https://www.tdcj.texas.gov/death_row" + cell.a.get('href'))
        else:
            this_row.append(cell.text)
    final.append(this_row)

with open("./output.csv", "w") as f:
    writer = csv.writer(f)
    for row in final:
        writer.writerow(row)
