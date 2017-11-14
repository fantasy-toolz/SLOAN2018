# -*- coding: utf-8 -*-
"""
Created on Fri Nov 03 19:52:15 2017

@author: Erich Rentz
"""

# boilerplate imports

import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import time

import matplotlib as mpl

import datetime
os.chdir(r'C:\US Solar\Scripts\MN\Xcel\20170621')

import os
dir = os.path.dirname(__file__)

# imports for scraping

from BeautifulSoup import BeautifulSoup
import requests

#teams = ['angels','astros','athletics','bluejays','braves',
#        'brewers','cardinals','cubs','diamondbacks','dodgers',
#        'giants','indians','mariners','marlins','mets','nationals',
#        'orioles','padres','phillies','pirates','rangers',
#        'rays','reds','redsox','rockies','royals','tigers','twins',
#        'whitesox','yankees']

teams = {'angels':  'LAA',
         'astros':  'HOU',
         'athletics':  'OAK',
         'bluejays':  'TOR',
         'braves':  'ATL',
         'brewers':  'MIL',
         'cardinals':  'STL',
         'cubs': 'CHC' ,
         'diamondbacks': 'ARZ' ,
         'dodgers':  'LAD',
         'giants':  'SF',
         'indians':  'CLE',
         'mariners':  'SEA',
         'marlins':  'MIA',
         'mets':  'NYM',
         'nationals':  'WSH',
         'orioles':  'BAL',
         'padres':  'SD',
         'phillies':  'PHI',
         'pirates':  'PIT',
         'rangers':  'TEX',
         'rays':  'TB',
         'reds':  'CIN',
         'redsox': 'BOS' ,
         'rockies':  'COL',
         'royals':  'KC',
         'tigers':  'DET',
         'twins':  'MIN',
         'whitesox': 'CHW' ,
         'yankees':  'NYY'}

#
# make hitter dictionary
#
HDict = {}

for team in teams:
    #print team
    #print teams[team]
    get_url = 'http://www.fangraphs.com/teams/'+team#angels'
    r  = requests.get(get_url)
    soup = BeautifulSoup(r.content)
    table_data      = soup.findAll("table")
    table_data = table_data[5]
    for row in table_data.findAll("tr"):
        for td in row.findAll("td"):       
            sav = td.find('a')   
            try:
                need_url = sav.get('href')
                print need_url
                print sav.text
                sav2 = [td.getText() for td in row.findAll("td")]          
#                 Apply a PA cut?
                if float(sav2[3]) > 0.:
                    HDict[sav.text] = str(need_url[(need_url).find('playerid')+9:(need_url).find('&')]), teams[team]            
            except:
                pass
            
#
# update hitter data
#

f = open(os.path.join(dir, 'data/batterdict.dat'),'w')

for entry in HDict.keys():
    try:
        print >>f,entry,'|', HDict[entry][1],'|',HDict[entry][0]
    except:
        print entry,'|',HDict[entry]
    

f.close()

#
# make pitcher dictionary
#
PDict = {}

for team in teams:
    #print team
    #print teams[team]
    get_url = 'http://www.fangraphs.com/teams/'+team#angels'
    r  = requests.get(get_url)
    soup = BeautifulSoup(r.content)
    table_data      = soup.findAll("table")
    table_data = table_data[6]
    for row in table_data.findAll("tr"):
        for td in row.findAll("td"):       
            sav = td.find('a')   
            try:
                need_url = sav.get('href')
                print need_url
                print sav.text
                sav2 = [td.getText() for td in row.findAll("td")]
                PDict[sav.text] = str(need_url[(need_url).find('playerid')+9:(need_url).find('&')]), teams[team]            
            except:
                pass
            
#
# update pitcher data
#

f = open(os.path.join(dir, 'data/pitcherdict.dat'),'w')

for entry in PDict.keys():
    try:
        print >>f,entry,'|', PDict[entry][1],'|',PDict[entry][0]
    except:
        print entry,'|',PDict[entry]
    

f.close()

#
# Create Fangraphs 2 Fox Batter Equivalencies CSV
#
hdict_df = pd.DataFrame.from_dict(HDict, orient='index')
hdict_df['Player'] = hdict_df.index
hdict_df.columns = ["ID", "Team", "Player"]
hdict_df["Fox Name"] = hdict_df["Player"].str.split(" ").str[-1]+", " + hdict_df["Player"].str.split(" ").str[0].str[0]+"."
hdict_df.to_csv(r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\batter name test.csv", index = False)

#
# Create Fangraphs 2 Fox Batter Equivalencies CSV
#
pdict_df = pd.DataFrame.from_dict(PDict, orient='index')
pdict_df['Player'] = pdict_df.index
pdict_df.columns = ["ID", "Team", "Player"]
pdict_df["Fox Name"] = pdict_df["Player"].str.split(" ").str[-1]+", " + pdict_df["Player"].str.split(" ").str[0].str[0]+"."
pdict_df.to_csv(r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\pitcher name test.csv", index = False)

#
# Import Fangraphs 2 Fox Equiv as DF
#
# Import Fangraphs Equivalency
name_equiv  = r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\DL Name Key.xlsx"
xl      = pd.ExcelFile(name_equiv)
equiv_df = xl.parse(xl.sheet_names[0])
equiv_df = equiv_df[["Fox Name", "Team", "ID"]]

#
#get unique player list
#
plist = HDict.keys()
pidlist = []
for p in plist:
    pidlist.append(HDict[p][0])

#
# Set Unique Day List
#
zero_day = 75 # 3/16/2017
max_day = 300

#
# Create DL Dict
#
DayStats = {}
DayStats['BooleanMask'] = {}

player = '5417'
#for unique player:
pnum = 0
for player in pidlist:
    #	query player up dates
    player_up_df = hdict_df.loc[hdict_df['ID'] == player]
    #	query player down dates
    status = 1
    DayStats['BooleanMask'][player] = np.zeros(max_day-zero_day,dtype=int)
    for day in range(zero_day, max_day+1):
        

#		calculate up date
#		calculate down date
#		if  down date is empty and  up date is empty
#			fill matrix with status
#		if up date is empty and down date is > day
#			fill matrix with status
#		if player down is empty and player up > day
#			status = 0
#			fill matrix with status
#		if down date > day 
#			fill matrix with status
#		if down date = day
#			status = 0 
#			calculate new down date
#			fill matrix
#		if up date = day
#			status = 1
#			calculate new up date
#			fill matrix

#dt = datetime.strptime("2017.03.16", "%Y.%m.%d")
#day_of_year = (dt - datetime(dt.year, 1, 1))
#day_of_year = dt.timetuple().tm_yday

daynum = int(datetime.datetime(int(sav[0].split('-')[0]),int(sav[0].split('-')[1]), int(sav[0].split('-')[2]), 0, 0, 0).timetuple().tm_yday) - zero_day

def obtain_players(plist):
    
    # set up dictionary
    DayStats = {}
    DayStats['PA'] = {}
    DayStats['R'] = {}
    DayStats['RBI'] = {}
    DayStats['H'] = {}
    DayStats['SB'] = {}
    DayStats['BB'] = {}
    DayStats['SO'] = {}
    DayStats['HR'] = {}
    



    for player in plist:
        
        
        DayStats['PA'][player] = np.zeros(max_day-zero_day,dtype=int)
        DayStats['R'][player] = np.zeros(max_day-zero_day,dtype=int)
        DayStats['RBI'][player] = np.zeros(max_day-zero_day,dtype=int)
        DayStats['H'][player] = np.zeros(max_day-zero_day,dtype=int)
        DayStats['SB'][player] = np.zeros(max_day-zero_day,dtype=int)
        DayStats['BB'][player] = np.zeros(max_day-zero_day,dtype=int)
        DayStats['SO'][player] = np.zeros(max_day-zero_day,dtype=int)
        DayStats['HR'][player] = np.zeros(max_day-zero_day,dtype=int)
        
        get_url = 'http://www.fangraphs.com/statsd.aspx?playerid='+str(HDict[player].strip())
        r  = requests.get(get_url); data = r.text; soup = BeautifulSoup(data); tables = soup.findAll('table')

        for indx,table in enumerate(tables):

            #print indx,[th.get_text() for th in table.find("tr").find_all("th")]

            if [th.get_text() for th in table.find("tr").find_all("th")] == itable:

                #print get_url
                if (pnum % 1) == 0:
                    print(pnum,player)

                pnum += 1
                dflag = 1

                for row in table.find_all("tr")[1:]:
                    
                    if (row in table.find_all("tr", class_="grid_postseason")) |\
                        (row in table.find_all("tr", class_="grid_multi")):
                            #print 'Multi and/or Postseason:',sav[0]
                            continue

                    sav = [td.get_text() for td in row.find_all("td")]
                    
                    if ('Date' not in sav[0]) & ('Total' not in sav[0]) :
                                            
                        daynum = int(datetime.datetime(int(sav[0].split('-')[0]),int(sav[0].split('-')[1]), int(sav[0].split('-')[2]), 0, 0, 0).timetuple().tm_yday) - zero_day

                        DayStats['PA'][player][daynum] = int(sav[5])
                        DayStats['R'][player][daynum] = int(sav[10])
                        DayStats['RBI'][player][daynum] = int(sav[11])
                        DayStats['H'][player][daynum] = int(sav[6])
                        DayStats['SO'][player][daynum] = int(np.round(0.01*float(sav[15].strip('%'))*float(sav[5]),0))
                        DayStats['BB'][player][daynum] = int(np.round(0.01*float(sav[14].strip('%'))*float(sav[5]),0))
                        DayStats['SB'][player][daynum] = int(sav[12])
                        DayStats['HR'][player][daynum] = int(sav[9])


        if dflag == 0:
            get_url = 'http://www.fangraphs.com/statsd.aspx?playerid='+str(HDict[player].strip())+'&position=PB'
            r  = requests.get(get_url); data = r.text; soup = BeautifulSoup(data); tables = soup.findAll('table')

            for indx,table in enumerate(tables):

                #print indx,[th.get_text() for th in table.find("tr").find_all("th")]

                if [th.get_text() for th in table.find("tr").find_all("th")] == itable:

                    print('Successfully read pitcher',player)

                    #print get_url
                    if (pnum % 1) == 0:
                        print(pnum,player)

                    pnum += 1

                    for row in table.find_all("tr")[1:]:

                        if (row in table.find_all("tr", class_="grid_postseason")) |\
                            (row in table.find_all("tr", class_="grid_multi")):
                                #print 'Multi and/or Postseason:',sav[0]
                                continue

                        sav = [td.get_text() for td in row.find_all("td")]

                        if ('Date' not in sav[0]) & ('Total' not in sav[0]) :

                            daynum = int(datetime.datetime(int(sav[0].split('-')[0]),int(sav[0].split('-')[1]), int(sav[0].split('-')[2]), 0, 0, 0).timetuple().tm_yday) - zero_day

                            DayStats['PA'][player][daynum] = int(sav[5])
                            DayStats['R'][player][daynum] = int(sav[10])
                            DayStats['RBI'][player][daynum] = int(sav[11])
                            DayStats['H'][player][daynum] = int(sav[6])
                            DayStats['SO'][player][daynum] = int(np.round(0.01*float(sav[15].strip('%'))*float(sav[5]),0))
                            DayStats['BB'][player][daynum] = int(np.round(0.01*float(sav[14].strip('%'))*float(sav[5]),0))
                            DayStats['SB'][player][daynum] = int(sav[12])
                            DayStats['HR'][player][daynum] = int(sav[9])


        if (pnum % 25) == 0:
            print('Executed in {0:4.5f} seconds\n'.format(time.time()-t0))
            
        #print('{0:4.5f} s'.format(time.time()-t1),end='')

    return DayStats


DStats = obtain_players(plist)































