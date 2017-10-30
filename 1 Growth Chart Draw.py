# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 15:06:32 2017

@author: Erich
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import matplotlib as mpl
import datetime

batterdict_dat = r"C:\Users\Erich\Documents\GitHub\SLOAN2018\data\batterdict.dat"
gamelogs_dat = r"C:\Users\Erich\Documents\GitHub\SLOAN2018\data\gamelogs.dat"
in_player = 'Anthony Rendon'
in_stat = 'PA'
day_range = range(0,226)
zero_day = 75
max_day = 300

# Support functions
def Remove_Name_Spaces(c):
  player_name = c['Player']
  player_name = " ".join(player_name.split())
  return player_name

# Import Batter Dict
batter_info_df = pd.read_table(batterdict_dat, 
                 sep="|", 
                 skiprows=0,  
                 names=['Player','ID'])

batter_info_df['Player'] = batter_info_df.apply(Remove_Name_Spaces, axis=1)

#for index, row in batter_info_df.iterrows():
#    if row[0][-1] == ' ':
#        print "Space Error"

# Import Gamelogs
cols = ['Stat','Player']
for i in day_range:
    cols.append("Day {0}".format(i))

gamelogs_df = pd.read_table(gamelogs_dat, 
                 sep=";", 
                 skiprows=0,  
                 names=cols)

gamelogs_df['Player'] = gamelogs_df.apply(Remove_Name_Spaces, axis=1)
#gamelogs_df['Stat'] = gamelogs_df.apply(Remove_Name_Spaces, axis=1)

#for index, row in df.iterrows():
#    if row[0][-1] == ' ':
#        print "Space Error"

# Query Player
new_df = gamelogs_df.loc[(gamelogs_df['Player'] == in_player) & (gamelogs_df['Stat'] == '{0} '.format(in_stat))]
new_df = new_df.drop('Stat', 1)
temp_list = list(new_df.iloc[0])

# Transpose
out_xy_list = []
for day in day_range:
    out_xy_list.append([day, temp_list[day]])
out_df = pd.DataFrame(out_xy_list, columns=['Day', in_stat])

# Plot
plt.plot(playerDF['Week'], playerDF[in_stat], 'x', color= 'k')
plt.title('{0} - {1}'.format(in_player, in_stat))


f = open(gamelogs_dat)

DDStats = {}

for line in f:
    q = [d.strip(" ") for d in line.split(';')]
    
    if q[0] not in DDStats.keys():
        DDStats[q[0]] = {}
        
    if q[1] not in DDStats[q[0]].keys():
        DDStats[q[0]][q[1]] = np.zeros(max_day-zero_day)
        
    for indx in range(0,len(q)-3):
        DDStats[q[0]][q[1]][indx] = float(q[indx+2])
    


f.close()


print(DDStats.keys())

PAlist = np.zeros([len(np.array(DDStats['PA'].keys())),max_day-zero_day])


stat = 'RBI'
print(len(np.array(DDStats[stat].keys())) )

for indx,player in enumerate(DDStats[stat].keys()):
    PAlist[indx] = np.cumsum(DDStats[stat][player])


fig = plt.figure()
ax = fig.add_axes([0.18,0.22,0.6,0.7])
ax2 = fig.add_axes([0.81,0.22,0.02,0.7])

    
    
for perc in range(100,0,-10):
    ax.plot(np.percentile(PAlist,perc,axis=0),color=cm.gnuplot(float(perc/100.),1.))
    

ax.plot(np.cumsum(DDStats[stat]['Mike Trout']),color='black')

    
ax.set_ylabel('RBIs',size=18)
ax.set_xlabel('Gameday Number',size=18)
    
cmap = mpl.cm.gnuplot; norm = mpl.colors.Normalize(vmin=0, vmax=100)
cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,norm=norm)
cb1.set_label('Percentile',size=18)







