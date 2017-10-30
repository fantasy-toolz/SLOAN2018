# Let's start by importing some site packages shall we?
# These packages will assist in webscraping
import requests
from BeautifulSoup import BeautifulSoup
# These packages are for tabular manipulation
import pandas as pd
import numpy as np
# These packages are for graphing
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# This is how the KMeans Sausage is made
from sklearn.cluster import KMeans
# This is a hack to make sure my IDE will display my Tables!
import sys;
sys.setrecursionlimit(40000)


url      =   "http://www.foxsports.com/mlb/transactions?year={0}&month={1}&type={2}"
months = range(0,12)
dl_types = [25, #15
            30, #60
            65, # 7
            76] # 10

# Grab 2016 Data
rows = []
for month in months:
    for dl in dl_types:
        year_url = url.format(str(2016), str(month), str(dl))
#        year_url = url.format(str(2017), str(4), str(0))
        r               = requests.get(year_url)
        soup            = BeautifulSoup(r.content)
#        text_file = open("Output2.txt", "w")
#        text_file.write(str(soup))
#        text_file.close()
        paginatory      = soup.find("div", { "class" : "wisbb_paginator"}) 
        if paginatory != None:
            for anchor in paginatory.findAll('a'):
                print year_url
                print anchor.text
        table_data      = soup.find("table", { "class" : "wisbb_standardTable wisbb_altRowColors"})   
        if table_data == None:
            pass
        else: 
            headers = [header.text for header in table_data.findAll('th')]
            # All of our data is in a 'Beautiful Soup' but we think in tables so let's coerce this data into a shape
            for row in table_data.findAll("tr"):
                cells = row.findAll("td")
                if len(cells) == 4:
                    new_row = []
                    for anchor in cells[0].findAll('a'):
                         new_row.append(anchor.text)
                    for anchor in cells[1].findAll('a'):
                         new_row.append(anchor.text)
                    for i in cells[2:]:
                        new_row.append(i.find(text=True))
                    new_row.append(dl)
                    new_row.append(month)
                    rows.append(new_row)

# Damn that was a shit way to do things. Strip out the unnecessary stuff.
strip_rows = []
for row in rows:
    strip_rows.append([str(row[1]),
                       str(row[3]),
                       str(row[4]),
                       str(row[5]),
                       row[6],
                       row[7]])

## Great, our Data is in a list of lists: much more pythonic. Let's birth a pandas table!
headers.append("DL Code")
headers.append("Month")
df16 = pd.DataFrame(strip_rows, columns=headers)
df16['Date Time'] = pd.to_datetime(df16['Date']+"/2016")

rows = []
for month in months[:10]:
    for dl in dl_types:
        year_url = url.format(str(2017), str(month), str(dl))
#        year_url = url.format(str(2017), str(4), str(0))
        r               = requests.get(year_url)
        soup            = BeautifulSoup(r.content)
#        text_file = open("Output2.txt", "w")
#        text_file.write(str(soup))
#        text_file.close()
        paginatory      = soup.find("div", { "class" : "wisbb_paginator"}) 
        if paginatory != None:
            for anchor in paginatory.findAll('a'):
                print year_url
                print anchor.text
        table_data      = soup.find("table", { "class" : "wisbb_standardTable wisbb_altRowColors"})   
        if table_data == None:
            pass
        else: 
#            headers = [header.text for header in table_data.findAll('th')]
            # All of our data is in a 'Beautiful Soup' but we think in tables so let's coerce this data into a shape
            for row in table_data.findAll("tr"):
                cells = row.findAll("td")
                if len(cells) == 4:
                    new_row = []
                    for anchor in cells[0].findAll('a'):
                         new_row.append(anchor.text)
                    for anchor in cells[1].findAll('a'):
                         new_row.append(anchor.text)
                    for i in cells[2:]:
                        new_row.append(i.find(text=True))
                    new_row.append(dl)
                    new_row.append(month)
                    rows.append(new_row)

# Damn that was a shit way to do things. Strip out the unnecessary stuff.
strip_rows = []
for row in rows:
    strip_rows.append([str(row[1]),
                       str(row[3]),
                       str(row[4]),
                       str(row[5]),
                       row[6],
                       row[7]])

## Great, our Data is in a list of lists: much more pythonic. Let's birth a pandas table!
df17 = pd.DataFrame(strip_rows, columns=headers)
df17['Date Time'] = pd.to_datetime(df17['Date']+"/2017")

# Let's take a look at these as histograms
import numpy
from matplotlib import pyplot

x = list(df17['Month'])
y = list(df16['Month'])

pyplot.hist(y, label='2016')
pyplot.hist(x, label='2017')
pyplot.legend(loc='upper right')
pyplot.show()

# Summary
summary_Table17 = df17.groupby("DL Code", as_index=False)['Date'].count()
summary_Table16 = df16.groupby("DL Code", as_index=False)['Date'].count()