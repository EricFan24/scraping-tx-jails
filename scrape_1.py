import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.tdcj.texas.gov/death_row/dr_offenders_on_dr.html")
html = response.content

print(html)
