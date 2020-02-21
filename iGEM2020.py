
# Imports
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
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
# End of imports



# Entrez email
Entrez.email = "rose.keenan@temple.edu"

# Collect and parse first page
page = requests.get('http://130.235.244.92/bcgi/malaviReport.cgi?report1=Grand+Lineage+Summary')
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the link div
link_text = soup.find(id='link')

# Pull text from all instances of <a> tag within link div
link_items = link_text.find('a')

# Grab the download link
suf = link_items.get('href')
suf = suf[2:]
url = 'http://130.235.244.92'  + suf

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

# rearranging columns
df = df[['NCBI Code', 'MalAvi Code', 'Avian Orden', 'Avian Family', 'Avian Genus', 'Avian Species', 'Avian Host Status (Migratory or Resident)', 'Vector Orden',
         'Vector Family', 'Vector Genus', 'Vector Species', 'Parasite Genus', 'Parasite Subgenus', 'Parasite Species', 'Continent' , 'Country' , 'Locality' , 'Year' , 
         'Reference', 'Sequence']]


df = df.drop_duplicates(subset='NCBI Code')

# Sets index to NCBI code
df.set_index('NCBI Code', inplace=True, drop=True, verify_integrity=True)


# Converts to list
code_list = df.index.tolist()
code_list = map(str, code_list)
code_list = list(map(str, code_list))

# Removing invalid codes
for value in code_list:
    value = value.split()
    if '\xa0' in value:
        value = value.replace('\xa0', '')

code_list = [value for value in code_list if len(value) == 8]

# Test list
my_list = ['JX418179','JX418219','MK061667','EF380150','KP347699','DQ659573','KP406597','KU562769']

# Parsing through records
fetchhandle = Entrez.efetch(db="nucleotide", id=code_list[0], rettype="gb")
records = list(SeqIO.parse(fetchhandle, "genbank"))
print(records)
print("\n")

for count in records:
    print(count)
    print('\n')

    print(count.description)
    print("\n")

    annotations = count.annotations
    print(annotations)
    print("\n")
    print(annotations['source'])
    print("\n")

    sequence = count.seq
    print('sequence: ' + sequence)
    print("\n")

    source = annotations['source']
    print("source: " + source)

    # Inserting a value into dataframe
    name = count.name
    print("name: " + name)
    df.loc[name, 'Sequence'] = sequence

fetchhandle.close()

# convert to csv
df.to_csv('grand-lineage-summary.csv', sep = '\t', encoding = 'utf-8', index = True)