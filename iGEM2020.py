
# imports
import webbrowser
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request
import pdb
import pandas as pd
import os
import numpy as np
import Bio
from Bio import Entrez

# Entrez email
Entrez.emial = "rose.keenan@temple.edu"

# Collect and parse first page
page = requests.get('http://130.235.244.92/bcgi/malaviReport.cgi?report1=Grand+Lineage+Summary')
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the link div
link_text = soup.find(id='link')

# Pull text from all instances of <a> tag within link div
link_items = link_text.find('a')

#grab the download link

suf = link_items.get('href')
suf = suf[2:]

url = 'http://130.235.244.92'  + suf
print(url)

# downloading using urllib
urllib.request.urlretrieve(url, 'grand-lineage-summary.csv')
          
# Read the csv file
df = pd.read_csv('grand-lineage-summary.csv', delimiter ='\t')

# removing unnecessary columns
df = df.drop(['Number_of_vectors', 'hosts', 'genera', 'length', 'families', 'orders', 'passerine',
                                                'Europe', 'South_Sahara', 'North_Africa_&_Middle_East', 'North_America', 'Hawaii', 'Central_America',
                                               'South_America', 'Asia', 'Australia_&_New_Zeeland', 'Oceania', 'Antarctica', 'Unknown'], axis=1)

# list of columns to be added
add_columns = ['Avian Orden', 'Avian Family', 'Avian Host Status (Migratory or Resident)', 'Vector Orden', 'Vector Family', 'Vector Genus', 'Vector Species' , 'Avian Genus' , 'Parasite Subgenus',
             'Avian Species' , 'Continent' , 'Country' , 'Locality' , 'Year' , 'Reference' ]

# adding appropriate columms
df = df.reindex(columns=df.columns.tolist() + add_columns)

# renaming columns
df.rename(columns = {'Lineage_Name' : 'MalAvi Code', 'accession' : 'NCBI Code', 'genus' : 'Parasite Genus', 'species' : 'Parasite Species', 'sequence' : 'Sequence'}, inplace = True)

# rearranging

df = df[['NCBI Code', 'MalAvi Code', 'Avian Orden', 'Avian Family', 'Avian Genus', 'Avian Species', 'Avian Host Status (Migratory or Resident)', 'Vector Orden',
         'Vector Family', 'Vector Genus', 'Vector Species', 'Parasite Genus', 'Parasite Subgenus', 'Parasite Species', 'Continent' , 'Country' , 'Locality' , 'Year' , 
         'Reference', 'Sequence']]

# convert to csv
df.to_csv('grand-lineage-summary.csv', sep = '\t', encoding = 'utf-8', index = False)


# MUST USE NCBI API FOR NEXT STEPS


# Focus on accession column only
#ncbi_page = 'https://www.ncbi.nlm.nih.gov/nuccore/' + df[['NCBI Code']].sample(1)


codes = df[['NCBI Code']]

code_list = df['NCBI Code'].tolist()

#output = [x.lower() for x in code_list]

#print(output)

while('Not sub' in code_list):
    code_list.remove('Not sub')

while(' ' in code_list):
    code_list.remove(' ')

while('nan' in code_list):
    code_list.remove('nan')

while('Not Sub' in code_list):
    code_list.remove('Not Sub')

print(code_list)



# Iterate through each row in the ncbiPage df to retrieve each link

for index, row in codes.iterrows():
    id = row['NCBI Code']
    print(id)
    fetch = Entrez.efetch(db="nuccore", id=id, rettype="gb", retmode="text")
    print(fetch.readline().strip())
    handle = Entrez.esummary(db="taxonomy", id=id, retmode="xml")
    records = Entrez.parse(handle)
    for record in records:
    # each record is a Python dictionary or list.
        print(record['Genus'])