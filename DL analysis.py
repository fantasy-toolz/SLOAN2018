
import requests
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd
from datetime import timedelta as td
# This is a hack to make sure my IDE will display my Tables!
import sys;
sys.setrecursionlimit(40000)


import os
#dir = os.path.dirname(__file__)

months      = range(1,12)
in_year     = '2017'
base_url    = "http://www.foxsports.com/mlb/transactions?year={0}&month={1}"
dl_code_dat = r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\DL Name Key.dat"
dl_code_xls = r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\DL Codes on Fox.xlsx"
name_equiv  = r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\DL Name Key 20171113.xlsx"
batter_dat  = r'C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\batterdict.dat'
unique_names_csv = r"C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\DL Name Key.csv"
boolean_dat = r'C:\Users\Erich Rentz\Documents\GitHub\SLOAN2018\data\booleanmask.dat'


def Write_Dict2DAT(in_dict, out_file):
    f = open(out_file,'w')
    for entry in in_dict.keys():
        try:
            print >>f,entry,'|', in_dict[entry]
        except:
            print entry,'|',in_dict[entry]
    f.close()
    
def Read_DAT2Dict(in_file, out_dict):
    out_dict = {}
    f = open(in_file)
    for line in f:
        try:
            out_dict[(line.split('|')[0]).strip()] = [line.split('|')[1].strip()]
        except:
            pass
    return out_dict

def Capture_all_DL_Codes(month_list):
    dl_codes = {}
    for month in month_list:
        year_url    = base_url.format(str(in_year), str(month))
        r           = requests.get(year_url)
        soup        = BeautifulSoup(r.content)
        paginatory  = soup.find("div", { "class" : "wisbb_paginator"})
        url_list    = [year_url]
        if paginatory != None:
            anchor_list = []
            for anchor in paginatory.findAll('a'):
                if len(anchor.text) < 5:
                    anchor_list.append(int(anchor.text))
            for anchor in range(min(anchor_list), max(anchor_list)+1):
                paginator_url = year_url + "&page={0}".format(anchor)
                url_list.append(paginator_url)       
        for url in url_list:
            print url
            r               = requests.get(year_url)
            soup            = BeautifulSoup(r.content)
            subject_options = [i.findAll('option') for i in soup.findAll('select', attrs = { "id" : "wisbb_ddltype"} )]
            for option in subject_options[0]:
                value_text = option['value'][40+len(str(month)):]
                if value_text != '0':
                    dl_codes[str(value_text)] = str(option.text)
    return dl_codes

def Read_DL_Code_UpDown(in_file):
    xl      = pd.ExcelFile(in_file)
    dl_code_df = xl.parse(xl.sheet_names[0])
    up_dict = {}
    down_dict = {}
    for index, row in dl_code_df.iterrows():
        if row[2] == 'Up':
            up_dict[row[0]]=row[1]
        if row[2] == 'Down':
            down_dict[row[0]]=row[1]
    return up_dict, down_dict

def Grab_Transaction_Data(in_year, month_list, in_transaction_list):
#    in_year = '2017'
#    month_list = [4]
#    in_transaction_list = [4]
    rows = []
    for month in month_list:
        for dl in in_transaction_list:
            year_url    = base_url.format(str(in_year), str(month))+ "&type={0}".format(str(dl))
            r           = requests.get(year_url)
            soup        = BeautifulSoup(r.content)
            paginatory  = soup.find("div", { "class" : "wisbb_paginator"}) 
            url_list    = [year_url]
            if paginatory != None:
                anchor_list = []
                for anchor in paginatory.findAll('a'):
                    if len(anchor.text) < 5: # Hack to deal with arrow special character, adjust if more than 9,999 transactions in period
                        anchor_list.append(int(anchor.text))
                for anchor in range(min(anchor_list), max(anchor_list)+1):
                    paginator_url = year_url + "&page={0}".format(anchor)
                    url_list.append(paginator_url)     
            for url in url_list:
                print url
                r               = requests.get(url)
                soup            = BeautifulSoup(r.content)    
                table_data      = soup.find("table", { "class" : "wisbb_standardTable wisbb_altRowColors"})   
                if table_data == None:
                    pass
                else: 
                    headers = [header.text for header in table_data.findAll('th')]
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
#                            print new_row
    strip_rows = []
    for row in rows:
        strip_rows.append([str(row[1]),
                           str(row[3]),
                           str(row[4]),
                           str(row[5]),
                           row[6],
                           row[7]])
    headers.append("DL Code")
    headers.append("Month")
    df = pd.DataFrame(strip_rows, columns=headers)
    df['Date Time'] = pd.to_datetime(df['Date']+"/{0}".format(in_year))
    return df


def UniqueNames4Equiv(in_up_df, in_down_df):
    ## Create Unique Name List CSV For Equiv
    unique_names = pd.concat([in_down_df, in_up_df])
    unique_names = unique_names.groupby(["Player", "Team"]).size()
    unique_names = pd.DataFrame(unique_names)
    unique_names['Player'] = unique_names.index
    unique_names["Name"] = unique_names["Player"].str[0]
    unique_names["Team"] = unique_names["Player"].str[1]
    unique_names = unique_names.reset_index(drop=True)
    unique_names = unique_names[['Name', 'Team']]
    unique_names.to_csv(unique_names_csv, index = False)
    
    #unique_names = up_transactions.groupby(["Player", "Team"]).size()
    #unique_names = pd.DataFrame(unique_names)
    #unique_names['Player'] = unique_names.index
    #unique_names["Name"] = unique_names["Player"].str[0]
    #unique_names["Team"] = unique_names["Player"].str[1]
    #unique_names = unique_names.reset_index(drop=True)
    #unique_names.columns = ['Up Transactions' , 'Player', 'Name', 'Team']
    #
    #unique_names2 = down_transactions.groupby(["Player", "Team"]).size()
    #unique_names2 = pd.DataFrame(unique_names2)
    #unique_names2['Player'] = unique_names2.index
    #unique_names2["Name"] = unique_names2["Player"].str[0]
    #unique_names2["Team"] = unique_names2["Player"].str[1]
    #unique_names2 = unique_names2.reset_index(drop=True)
    #unique_names2.columns = ['Down Transactions' , 'Player', 'Name', 'Team']
    #trans_counts = pd.merge(unique_names, unique_names2,  how='left', left_on='Player', right_on = 'Player')


def Run_Equiv_N_HDict(in_up_df, in_down_df, in_batter_dat):
    # Import Fox2Fangraphs Equiv Table
    xl      = pd.ExcelFile(name_equiv)
    equiv_df = xl.parse(xl.sheet_names[0])
    equiv_df = equiv_df[["Fox Name", "Team", "ID"]]
    # Join Equivaleny to up and down transactions
    up_equiv_df = pd.merge(in_up_df, equiv_df,  how='left', left_on=['Player','Team'], right_on = ['Fox Name','Team'])
    down_equiv_df = pd.merge(in_down_df, equiv_df,  how='left', left_on=['Player','Team'], right_on = ['Fox Name','Team'])
    # Open hitter list 'n Populate Dict
    HDict = {}
    f = open(in_batter_dat)
    for line in f:
        #print line
        try:
            HDict[(line.split('|')[0]).strip()] = [line.split('|')[2][:-1].strip(), line.split('|')[1].strip()]
        except:
            pass        
    print('Found {} hitters by scraping teams.'.format(len(HDict.keys())))
    return up_equiv_df, down_equiv_df, HDict

def Create_DayStatsDict(in_HDict, in_up_df, in_down_df):
    # Create Player List
    plist = in_HDict.keys()
    pidlist = []
    for p in plist:
        pidlist.append(in_HDict[p][0])
    # Set Epoch
    zero_day = 75 # 3/16/2017
    max_day = 300
    DayStats = {}
    DayStats['BooleanMask'] = {}
    ## Test Players
    #player = 'Jose Altuve'
    #player = 'Jason Castro'
    #player = 'Whit Merrifield'
    #player = 'Ian Desmond'
    #player = 'Homer Bailey'
    
    # Run DL Algorithm
    for player in plist:
        print "\n"+player
        # Get Fangraphs Player ID
        pid = in_HDict[player][0]
        #	query player up dates
        player_up_df = in_up_df.loc[in_up_df['ID'] == int(pid)] 
        #	query player down dates
        player_down_df = in_down_df.loc[in_down_df['ID'] == int(pid)]
        # Set the table
        status = 1
        DayStats['BooleanMask'][player] = np.zeros(max_day-zero_day,dtype=int)
        # Calculate Dates
        up_date = player_up_df['Date Time'].min().date()
        down_date = player_down_df['Date Time'].min().date()
        # Test For Players Currently Down
        cur_date = (datetime(2017, 1, 1)+  td(days=zero_day-1)).date()
        if down_date < cur_date:
            status = 0
        if down_date != down_date and up_date > cur_date:
            status = 0
        # Iterate Across Days
        for day in range(zero_day, max_day):
            cur_date = (datetime(2017, 1, 1)+  td(days=day-1)).date()
    #        print cur_date
            daynum = day - zero_day
            # if up date and down date are empty
            if down_date == cur_date:
                print  "Down {0}".format(cur_date),
                status = 0
                DayStats['BooleanMask'][player][daynum] = status
                player_down_df = player_down_df.loc[in_down_df['Date Time'] > cur_date]
                down_date = player_down_df['Date Time'].min().date()
            elif up_date == cur_date:
                print "Up {0}".format(cur_date),
                status = 1
                DayStats['BooleanMask'][player][daynum] = status
                player_up_df = player_up_df.loc[in_up_df['Date Time'] > cur_date]
                up_date = player_up_df['Date Time'].min().date()
            else:
                DayStats['BooleanMask'][player][daynum] = status
                print "{0}".format(status),
    return DayStats

def Write_Dict2Dat2(in_dict, out_dat):
    from __future__ import print_function
    f = open(out_dat,'w')
    for statkey in in_dict.keys():
        for player in in_dict[statkey].keys():
            print(statkey,';',player,';',end='',file=f)
            for daynum in range(0,len(in_dict[statkey][player])):    
                print(in_dict[statkey][player][daynum],';',end='',file=f)    
            print('',file=f)
    f.close()

def Main():
    # Get a Dictionary of all DL Codes and Save to Disc; Only run if need to update DL Codes
    dl_codes = Capture_all_DL_Codes(months[:11])
    Write_Dict2DAT(dl_codes, dl_code_dat)
    # Read in DL Code Up/Down Equivs
    up_code_dict, down_code_dict = Read_DL_Code_UpDown(dl_code_xls)
    up_types = up_code_dict.keys()
    down_types = down_code_dict.keys()
    # Run Up and Down Transactions Scrape
    up_transactions = Grab_Transaction_Data('2017', months[:10], up_types)
    down_transactions = Grab_Transaction_Data('2017', months[:10], down_types)
    # Unique Values for Equiv
    #
    # Create Up/Down Equivs and HDict
    up_equiv_df, down_equiv_df, HDict = Run_Equiv_N_HDict(up_transactions, down_transactions, batter_dat)
