import mechanize
import cookielib
import os
import csv
import numpy
import pandas as pd
import numpy as np
from scipy import interpolate
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

data_dir = r"C:\Fantasy\faWAR Disag\2016"
season_dir = r"C:\Fantasy\Growth Chart\Data"
csv_name_temp = "Week_{0}_Stats_{1}.csv"
cur_wk = 22
position_list       = ['C','1B','2B','3B','SS','OF', 'U']
username            =   ''
password            =   ''
base_path           =   r"C:\Fantasy\faWAR Disag\2017 v1" #the folder where the output csv are saved
url_path            =   "http://phidelt1.baseball.cbssports.com/print/csv/stats/stats-main/all:{0}/period-{1}:p/standard"

# Subroutines
def CreateBrowserObject():
    # Create Browser
    br = mechanize.Browser()
    # Cookie Jar probably not needed
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    # Format Browser Object
    br.set_handle_robots(False)
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', 'Chrome')]
    sign_in = br.open("https://auth.cbssports.com/login")
    br.select_form(nr = 0) #access form by their index
    # Populate Form
    br.form["userid"]       =  username   #CBS uses userid instead of the typical username
    br.form["password"]     =  password   
    br.form.new_control('hidden', 'dummy::login_form',   {'value': '1'})            
    br.form.new_control('hidden', 'form::login_form',   {'value': 'login_form'})
    br.form.new_control('hidden', 'xurl',   {'value': 'http://phidelt1.baseball.cbssports.com/'})
    br.form.new_control('hidden', 'master_product',   {'value': '150'})
    br.form.new_control('hidden', 'vendor',   {'value': 'cbssports'})
    # Log into the account
    logged_in = br.submit()   
    # Return the Browser Object
    return br

def Remove_Name_Spaces(c):
  player_name = c['Player']
  player_name = " ".join(player_name.split())
  return player_name

def simple_name(c):
    # strip out the team name
    line = c['Player'].split('|')
    player_name_position = line[0]
    player_name = " ".join(player_name_position.split()[:-1])
    return player_name

def DownloadData_SubRoutine(br, week, position):
    # Get URL Formatted
    week = str(week)
    report_page = url_path.format(position, week)
    new_report = br.open(report_page)
    # Create DataFrame
    df = pd.read_csv(new_report, skiprows=[0,-1], header=0)
    # Remove Last Line of DataFrame
    df = df[:-1]
    # Clean "Player" Field
    df['Player'] = df.apply(Remove_Name_Spaces, axis=1)
    df['Player'] = df.apply(simple_name, axis=1)
    # Drop Extra Fields
    drop_fields = ["Avail", "Unnamed: 18", "1B", "2B", "3B", "BB", "KO", "CS", "OBP", "SLG"]
    for f in drop_fields:
        df = df.drop(f, 1)
    # Query only the players who played
    df = df.loc[df['Rank'] != 9999]
    # Save Position/Week DataFrame to CSV
    report_csv = os.path.join(season_dir, "Week_"+week+"_Stats_"+str(position)+".csv")
    df.to_csv(report_csv, index=False)

def grab_player_data(pos_of_int, in_stat, in_player):
    # Set Range of Weeks For Data Dev
    wk_range = range(1,cur_wk+1)
    # Import Data for Each Week in Range
    for wk in wk_range:
        file_name = os.path.join(season_dir, csv_name_temp.format(wk, pos_of_int))
        if wk==1:
            df = pd.read_csv(file_name)
            df = df[['Player', '{0}'.format(in_stat)]]
            df.columns = ['Player', '{0} 1'.format(in_stat)]
        else:
            df1 = pd.read_csv(file_name)
            df1 = df1[['Player', '{0}'.format(in_stat)]]
            df1.columns = ['Player', '{0} {1}'.format(in_stat, wk)]
            df = df.merge(df1, how = 'outer', on = 'Player')
            df = df.fillna(0)
            df['{0} {1}'.format(in_stat, wk)] = df['{0} {1}'.format(in_stat, wk)]+df['{0} {1}'.format(in_stat, wk-1)]
    # Query Player
    new_df = df.loc[df['Player'] == in_player]
    temp_list = list(new_df.iloc[0])
    # Transpose
    out_xy_list = []
    for wk in wk_range:
        out_xy_list.append([wk, temp_list[wk]])
    out_df = pd.DataFrame(out_xy_list, columns=['Week', in_stat])
    return out_df  

# Routines
def DownloadAllData():
    # Create Browser Object
    br = CreateBrowserObject()
    # Iterate Acress Weeks
    for week in range(1, cur_wk+1):
        # Iterate Across Positions
        for position in position_list:  
            DownloadData_SubRoutine(br, week, position)

def dev_growth_chart(pos_of_int, in_stat, in_player):
    # Create Empty Lists for Data Import
    file_list = []
    long_data = []
    # Set Range of Weeks For Data Dev
    wk_range = range(1,19)
    # Import Data for Each Week in Range
    for wk in wk_range:
        file_name = os.path.join(data_dir, csv_name_temp.format(wk, pos_of_int))
        file_list.append(file_name)
        if wk==1:
            df = pd.read_csv(file_name)
            df = df[['Player', '{0}'.format(in_stat)]]
            df.columns = ['Player', '{0} 1'.format(in_stat)]
        else:
            df1 = pd.read_csv(file_name)
            df1 = df1[['Player', '{0}'.format(in_stat)]]
            df1.columns = ['Player', '{0} {1}'.format(in_stat, wk)]
            df = df.merge(df1, how = 'outer', on = 'Player')
            df = df.fillna(0)
            df['{0} {1}'.format(in_stat, wk)] = df['{0} {1}'.format(in_stat, wk)]+df['{0} {1}'.format(in_stat, wk-1)]
        if wk%4 == 0 or wk == 1 or wk ==18:
            long_data.append([wk, 
                              df['{0} {1}'.format(in_stat, wk)].quantile(.05), 
                              df['{0} {1}'.format(in_stat, wk)].quantile(.10),
                              df['{0} {1}'.format(in_stat, wk)].quantile(.25), 
                              df['{0} {1}'.format(in_stat, wk)].quantile(.5), 
                              df['{0} {1}'.format(in_stat, wk)].quantile(.75), 
                              df['{0} {1}'.format(in_stat, wk)].quantile(.90),
                              df['{0} {1}'.format(in_stat, wk)].quantile(.95)])
    
    # Develop DataFrame for Spline     
    quartile_df = pd.DataFrame(long_data, columns=['Week', '0.05','0.10', '0.25', '0.50', '0.75','0.90','0.95'])
    # Create Spline Functions for Percentile Lines
    f3 = interpolate.interp1d(quartile_df['Week'], quartile_df['0.50'])
    f4 = interpolate.interp1d(quartile_df['Week'], quartile_df['0.75'])
    f5 = interpolate.interp1d(quartile_df['Week'], quartile_df['0.90'])
    f6 = interpolate.interp1d(quartile_df['Week'], quartile_df['0.95'])
    # Calaculate Spline Curves
    xnew = np.arange(1, 18, .1)  
    ynew3 = f3(xnew)
    ynew4 = f4(xnew)
    ynew5 = f5(xnew)
    ynew6 = f6(xnew)
    # Draw Out Percentiles
    fig = plt.figure()
    plt.plot(xnew, ynew3, '-', color= 'b', alpha = 0.4)
    plt.plot(xnew, ynew4, '-', color= 'g', alpha = 0.4)
    plt.plot(xnew, ynew5, '-', color= 'c', alpha = 0.4)
    plt.plot(xnew, ynew6, '-', color= 'm', alpha = 0.4)
    # Adjust the images
    plt.text(16.5,f3(16.5),'50%', color= 'b', backgroundcolor= 'w', horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(16.5,f4(16.5),'75%', color= 'g', backgroundcolor= 'w', horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(16.5,f5(16.5),'90%', color= 'c', backgroundcolor= 'w', horizontalalignment = 'center', verticalalignment = 'center')
    plt.text(16.5,f6(16.5),'95%', color= 'm', backgroundcolor= 'w', horizontalalignment = 'center', verticalalignment = 'center')
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
    # Grab Player Data
    playerDF = grab_player_data(pos_of_int, in_stat, in_player)
    plt.plot(playerDF['Week'], playerDF[in_stat], 'x', color= 'k')
    plt.title('{0} - {1}'.format(in_player, in_stat))
    return fig

def Create_PlayerStat_LM(pos_of_int, in_stat, in_player, gen_fig):
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    playerDF = grab_player_data(pos_of_int, in_stat, in_player)
    # Reshape the Data
    x = playerDF['Week'].values
    y = playerDF[in_stat].values
    x = x.reshape(cur_wk, 1)
    y = y.reshape(cur_wk, 1)
    regr.fit(x, y)
    # Create Report
    report_info = {"Player": in_player,
                   "Slope":regr.coef_[0][0], 
                   "Intersect": regr.intercept_[0], 
                   "MAE": mean_absolute_error(y, regr.predict(x)),
                   "R^2" :regr.score(x, y)}
    if gen_fig:
        # Create Figure
        fig = plt.figure()
        reg_plot = fig.add_subplot(111)
        reg_plot.plot(x, regr.predict(x), color='blue', linewidth=1, linestyle = 'dashed')
        reg_plot.scatter(x, y,  marker = 'o', color= 'black')
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

# Get All Player Names
def AggregateByStatPosition(pos_of_int, in_stat):
    # Collect Downloaded Data
    week_position_dfs = []
    # Iterate Acress Weeks
    for week in range(1, cur_wk+1):
        week = str(week)
        # Import Position/Week DataFrame to CSV
        report_csv = os.path.join(season_dir, "Week_"+week+"_Stats_"+pos_of_int+".csv")    
        df = pd.read_csv(report_csv)
        week_position_dfs.append(df)
    # Aggregate All Data
    all_week_position = week_position_dfs[0]
    for df in week_position_dfs[1:]:
        all_week_position =  pd.concat([all_week_position, df])   
    season_player_df = all_week_position.groupby(["Player"], as_index=False)[in_stat].sum()
    # Run Linear Model For Every Player
    rows = []
    for index, row in season_player_df.iterrows():
        fig, player_dict = Create_PlayerStat_LM(pos_of_int, in_stat, row['Player'], False)
        # Convert Dict to DF
        headers = ['Player', 'Slope', 'R^2', 'MAE', "Intersect"]
        temp_df = pd.DataFrame([player_dict], columns=headers)
        rows.append(temp_df.values.tolist()[0])
    df = pd.DataFrame(rows, columns=headers)
    # Join Linear Model Data to Summary
    season_player_df = season_player_df.merge(df, on='Player')
    return season_player_df

# Download Data
DownloadAllData()

# Pass through some samples
dev_growth_chart('OF', 'R', 'Jose Ramirez')
dev_growth_chart('OF', 'R', 'Aaron Judge')
dev_growth_chart('SS', 'R', 'Elvis Andrus')
dev_growth_chart('SS', 'HR', 'Elvis Andrus')
dev_growth_chart('SS', 'RBI', 'Elvis Andrus')
dev_growth_chart('SS', 'SB', 'Elvis Andrus')
dev_growth_chart('OF', 'R', 'Cody Bellinger')
dev_growth_chart('1B', 'RBI', 'Mark Reynolds')
dev_growth_chart('1B', 'RBI', 'Albert Pujols')
dev_growth_chart('1B', 'RBI', 'Freddie Freeman')
dev_growth_chart('1B', 'RBI', 'Edwin Encarnacion')
dev_growth_chart('3B', 'RBI', 'Miguel Sano')
dev_growth_chart('3B', 'HR', 'Miguel Sano')
    
fig, charlie_dict = Create_PlayerStat_LM('OF', 'R', 'Charlie Blackmon', True)
fig, billy_dict = Create_PlayerStat_LM('OF', 'R', 'Billy Hamilton', True)
fig, joey_dict = Create_PlayerStat_LM('1B', 'R', 'Joey Votto', True)
fig, cespedes_dict = Create_PlayerStat_LM('OF', 'R', 'Yoenis Cespedes', True)

of_R_DF = AggregateByStatPosition('OF', 'R')

X = of_R_DF[['R','Slope', 'R^2', 'MAE', 'Intersect']].values
X_std = StandardScaler().fit_transform(X)

num_clusters = 7
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
kmeans.fit(X_std)
predict = kmeans.predict(X_std)

# I still see things better in tables, so I'll pop the cluster assignments back to the dataframe.
of_R_DF['Clusters'] = pd.Series(predict, index=of_R_DF.index)

# That tells us a bit, but we can get more with some graphs. Let's start in 2D graphing the BB/9 to FIP relationship.
colors = ["k.","r.", "c.","y.", "m.", "g.", "b."]

# Part of the clustering appeal is that it can handle a lot of dimensions. Indeed, we gave the clustering algorithm 3 dimensions.
# Let's take a look at how these clusters look in 3D by adding the K/9 totals as the z direction.
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(len(X)):
#    print("coordinate:",X[i], "label:", labels[i])
    ax.scatter(X[i][1], X[i][2], X[i][4], c = colors[labels[i]][0], linewidths = 0, alpha = 0.3)
fig

of_R_DF.to_csv(r"C:\Fantasy\Growth Chart\Data\Season OF R 20170920.csv", index=False)