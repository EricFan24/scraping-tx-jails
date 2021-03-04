import re # For letting us search for partial text 
import csv # For writing CSVs
import requests # For getting data off the internet
from time import sleep # For slowing our script down 
from bs4 import BeautifulSoup # For parsing HTML

. 
def scrape_detail(url):
    """
    This function takes a URL to a prisoner detail page and extracts
    the highest education level, returning it as a list. We could
    easily extend this to add more information
    """
    if "jpg" in url: # Some of the details are photos. We can skip those. 
        return [] # And when we do, we just return a blank list. 
    print(url) # For debugging and to give us some sense of time when we run it
    response = requests.get(url) # Get a response from the URL
    html = response.content # Get the HTML from the response
    soup = BeautifulSoup(html, features="html.parser") # Parse the response
    table = soup.find("table") # Get the first table
    grade_label = table.find('td', text=re.compile("Education Level*")) # Find a table cell that has "Education Level" in it
    grade = grade_label.find_next("td") # Get the next cell -- the one directly after it. 
    return [grade.text] # Return it as a single-item list


def get_data_for_row(row):
    """
    This function takes a table row from the Texas inmate table, extracts
    the data (including the URL to the detail page) and returns a list.
    """
    # Declare an empty list to fill with the columns for this row
    data = []
    # For every cell (or column) in the table
    for cell in row.findAll("td"):
        if cell.a: # Check to see if we're a link tag
            # If so, get the link text and make sure we have the full URL
            data.append("https://www.tdcj.texas.gov/death_row/" + cell.a.get('href'))
        else:
            # Otherwise, return the text of the cell
            data.append(cell.text)
    return data


# This makes our request to the main list URL
response = requests.get("https://www.tdcj.texas.gov/death_row/dr_offenders_on_dr.html")
# And gets the HTML from the response
html = response.content

# Parse the HTML from the response
soup = BeautifulSoup(html, features="html.parser")
# And get the first table
table = soup.find("table")

# We declare an empty final list where we'll stuff all of the data
# we want to write out to a CSV
final = []
# For every row in the table, except the header
for row in table.findAll("tr")[1:]:
    # Call our function to get the data from the table row
    row_data = get_data_for_row(row)
    # Call our function to scrape the detail page, using the URL we just extracted.
    # The += means we simply add the response from that function to our row's columns
    row_data += scrape_detail(row_data[1])
    # Pause the script for .01 seconds to give the server a breather.
    sleep(0.01)

    # Finally, append the row data, including what we scraped from the
    # detail page, to the final list.
    final.append(row_data)

# When that's all done, we open a file called "output.csv" in the current directory
with open("./output.csv", "w") as f:
    # Then we tell python we want to use this file to write a CSV to
    writer = csv.writer(f)
    # And we write all of the rows
    writer.writerows(final)
