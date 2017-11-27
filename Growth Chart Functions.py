# -*- coding: utf-8 -*-
"""
@author: Erich Rentz
"""

# boilerplate imports

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import matplotlib as mpl
import datetime
from sklearn import linear_model
from scipy.interpolate import spline
from sklearn.metrics import mean_absolute_error

min_GP = 50
zero_day = 75
max_day = 300
graph_percentiles = [95, 90, 75, 50, 25, 10, 5]

game_logs_dat = r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018-master\data\gamelogs.dat"

def Read_DAT2Dict(in_file):
    out_dict = {}
    f = open(in_file)
    for line in f:
        q = [d.strip(" ") for d in line.split(';')]
        
        if q[0] not in out_dict.keys():
            out_dict[q[0]] = {}
            
        if q[1] not in out_dict[q[0]].keys():
            
            if q[0] in ['OPP','POS','TEAM']:
                out_dict[q[0]][q[1]] = np.zeros(max_day-zero_day,dtype='S5')
                
            else:
                out_dict[q[0]][q[1]] = np.zeros(max_day-zero_day)
            
        for indx in range(0,len(q)-3):
            #print(q[0],q[1],q[indx+2])
            
            if q[0] in ['OPP','POS','TEAM']:
                out_dict[q[0]][q[1]][indx] = q[indx+2]
    
            else:
                try:
                    out_dict[q[0]][q[1]][indx] = float(q[indx+2])
                except:
                    out_dict[q[0]][q[1]][indx] = 0.
    f.close()
    return out_dict              

def graph_growth_chart_1(in_player, in_stat, in_dict, in_denominator = None, draw_all_players = None):
    # GP Length
    GP_len = 0
    # Determine the percentile universe
    if in_denominator:
        # Create empty list for player indices
        plist = []
        # set denominator
        deno_type = in_denominator.keys()[0]
        deno_query = in_denominator.values()[0]
        # Query based on input
        for indx,plr in enumerate(in_dict[deno_type].keys()):
            y = np.cumsum(in_dict[in_stat][plr])
            y = y[np.logical_not(np.isnan(y))]
            if len(y) > GP_len:
                GP_len = len(y)
            if len(np.where(in_dict[deno_type][plr] == deno_query)[0]) >= min_GP:
#                print plr
                plist.append(plr)
        # Create clean slate for player list then populate with stats for building percentiles
        PAlist = np.zeros([len(plist),GP_len])
        for indx,player in enumerate(np.array(plist)):
            PAlist[indx] = np.cumsum(in_dict[in_stat][player])[:GP_len]
    else:
        for indx,plr in enumerate(in_dict['PA'].keys()):
            y = np.cumsum(in_dict[in_stat][plr])
            y = y[np.logical_not(np.isnan(y))]
            if len(y) > GP_len:
                GP_len = len(y)
        PAlist = np.zeros([len(np.array(in_dict['PA'].keys())),GP_len])
        # For Player in Stat Keys, fill empty slate
        for indx,player in enumerate(in_dict[in_stat].keys()):
            PAlist[indx] = np.cumsum(in_dict[in_stat][player])[:GP_len]
#    print "This is the GP: {0}".format(GP_len)
    # Create Grap Object and add axes
    fig = plt.figure()
    ax = fig.add_axes([0.18,0.22,0.6,0.7])
    ax2 = fig.add_axes([0.81,0.22,0.02,0.7])
    if draw_all_players:
        for index in PAlist:
            ax.plot(index,color='grey')
    # Draw Percentiles
#    for perc in graph_percentiles:
    for perc in range(100,0,-10):
        ax.plot(np.percentile(PAlist,perc,axis=0),color=cm.gnuplot(float(perc/100.),1.))
    # Draw Player Profile
    ax.plot(np.cumsum(in_dict[in_stat][in_player]),color='black')
    # Add Labels    
    ax.set_ylabel(in_stat,size=18)
    ax.set_xlabel('Gameday Number',size=18)
    cmap = mpl.cm.gnuplot; norm = mpl.colors.Normalize(vmin=0, vmax=100)
    cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,norm=norm)
    cb1.set_label('Percentile',size=18)

def graph_growth_chart_2(in_player, in_stat, in_dict, gen_fig=True): 
    # Grab Stats 
    y = np.cumsum(in_dict[in_stat][in_player])
    y = y[np.logical_not(np.isnan(y))]
    x = np.array(range(0,len(y))) 
    # Reshape the Data
    x = x.reshape(len(y), 1)
    y = y.reshape(len(y), 1)
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Fit a line to Data
    regr.fit(x, y)
    # Create Report
    report_info = {"Player": in_player,
                   "Slope":regr.coef_[0][0], 
                   "Intersect": regr.intercept_[0], 
                   "MAE": mean_absolute_error(y, regr.predict(x)),
                   "R^2" :regr.score(x, y)}
    # Determine whether to graph or not
    if gen_fig:
        # Create Figure, plot, and scatter
        fig = plt.figure()
        reg_plot = fig.add_subplot(111)
        reg_plot.plot(x, regr.predict(x), color='blue', linewidth=1, linestyle = 'dashed')
        reg_plot.scatter(x, y,  marker = 'o', color= 'black')
        # Add some graph junk
        plt.tick_params(
                axis='x',
                which='both',
                bottom='off',
                top='off')
        plt.xlabel("Week")
        plt.tick_params(
                axis='y',
                which='both',
                left='off',
                right='off')
        plt.title('{0} - {1}'.format(in_player, in_stat))
        # Add Blurb to Image
        plt.text(1, max(y), 'Slope: {0}\nIntersect: {1}\nMAE: {2}\nR^2: {3}'.format(round(report_info['Slope'], 2), 
                 round(report_info['Intersect'],2), round(report_info['MAE'],2), round(report_info['R^2'],2)), verticalalignment  = 'top')
        return fig, report_info
    else:
        return "No Figure", report_info    

def graph_growth_chart_3(in_player, in_stat, in_dict, gen_fig=True, window_size = 7):   
    # Grab Stats 
    y = np.cumsum(in_dict[in_stat][in_player])
    y = y[np.logical_not(np.isnan(y))]
    x = np.array(range(0,len(y))) 
    # Reshape the Data
    x = x.reshape(len(y), 1)
    y = y.reshape(len(y), 1)
    # Create Base Plot and scatter
    fig = plt.figure()
    reg_plot = fig.add_subplot(111)
    reg_plot.scatter(x, y,  marker = 'o', color= 'black')
    # Create linear regression object and list for final regressions
    regr = linear_model.LinearRegression()
    reg_list = []
    # Calculate last day and define start date
    final_day = len(y)
    premier_date = 14
    # Run through days creating a moving window linear regression across the longitudinal data
    for day in range(premier_date, len(y), window_size):
        regr = linear_model.LinearRegression()
        start_day = day
        stop_day = day+7
        if stop_day < final_day:
            sub_x = x[start_day:stop_day]
            sub_y = y[start_day:stop_day]
            sub_x = sub_x.reshape(start_day-stop_day+1,1)
            sub_y = sub_y.reshape(start_day-stop_day+1,1)
            regr.fit(sub_x, sub_y)
            reg_list.append(regr) 
    # Run through windows graphing the linear models 
    day = premier_date
    for lm in reg_list:
        start_day = day-(window_size+2)
        stop_day = day + (window_size+2)
        if stop_day < final_day:
            sub_x = x[start_day:stop_day]
            sub_y = y[start_day:stop_day]
            sub_x = sub_x.reshape(start_day-stop_day+1,1)
            sub_y = sub_y.reshape(start_day-stop_day+1,1)
            reg_plot.plot(sub_x, lm.predict(sub_x), color='red', linewidth=1, linestyle = '-')
            day = day+window_size
    # Add some graph junk
    plt.tick_params(
            axis='x',
            which='both',
            bottom='off',
            top='off')
    plt.xlabel("Games Played")
    plt.tick_params(
            axis='y',
            which='both',
            left='off',
            right='off')
    plt.title('{0} - {1}'.format(in_player, in_stat))
    return fig

#
##### Main

# Grab DDD Stats from game logs dat
DDStats = Read_DAT2Dict(game_logs_dat)
print(DDStats.keys())

# Re-organize by game
GStats = {}

for key1 in DDStats.keys():
    
    GStats[key1] = {}
    
    for key2 in DDStats[key1].keys():
        
        if key1 in ['OPP','POS','TEAM']:
            GStats[key1][key2] = np.zeros(max_day-zero_day,dtype='S5')
            
        else:
            GStats[key1][key2] = np.zeros(max_day-zero_day) + np.nan
#            GStats[key1][key2] = np.zeros(max_day-zero_day) + 0
        gnum = 0
        for indx,val in enumerate(DDStats[key1][key2]):
            
            if DDStats['POS'][key2][indx] != '':
                GStats[key1][key2][gnum] = DDStats[key1][key2][indx]
                gnum += 1

# Create Growth Chart 1 Samples
graph_growth_chart_1('Adam Jones', 'R',  GStats)
temp_dict = {'POS':'1B'}
graph_growth_chart_1('Joey Votto', 'R', GStats, temp_dict)

# Create Growth Chart 2 Samples
graph_growth_chart_2('Adam Jones', 'R',  GStats, gen_fig=True)
graph_growth_chart_2('Jose Altuve', 'R',  DDStats, gen_fig=True)
graph_growth_chart_2('Alcides Escobar', 'R',  DDStats, gen_fig=True)   
graph_growth_chart_2('Corey Dickerson', 'R',  DDStats, gen_fig=True)
graph_growth_chart_2('Whit Merrifield', 'R',  DDStats, gen_fig=True)
graph_growth_chart_2('Domingo Santana', 'R',  DDStats, gen_fig=True)
graph_growth_chart_2('Mallex Smith', 'R',  DDStats, gen_fig=True)

# Create Growth Chart 3 Samples
graph_growth_chart_3('Whit Merrifield', 'R',  DDStats, gen_fig=True)
graph_growth_chart_3('Domingo Santana', 'R',  DDStats, gen_fig=True)
graph_growth_chart_3('Mallex Smith', 'R',  DDStats, gen_fig=True)


















