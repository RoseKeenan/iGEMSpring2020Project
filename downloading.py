import webbrowser
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request
import pdb
import pandas as pd
import numpy as np
import Bio

# Collect and parse first page
page = requests.get('http://130.235.244.92/bcgi/malaviReport.cgi?report1=Grand+Lineage+Summary')
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the link div
linkText = soup.find(id='link')

# Pull text from all instances of <a> tag within link div
linkItems = linkText.find('a')

#grab the download link

suf = linkItems.get('href')
suf = suf[2:]

url = 'http://130.235.244.92'  + suf
print(url)

# downloading using urllib
urllib.request.urlretrieve(url, "grand-lineage-summary.xls")

# downloading using requests
#text = requests.get(url).text

#import pdb;
#pdb.set_trace()

# open method to open a file on your system and write the contents
#with open("grand-lineage-summary.xls", "w") as code:
#    code.write(text)
    