import os
import matplotlib.pyplot as pyplot
import seaborn as sns
import pandas as pd 
import numpy as np 
import requests
import configparser as cp
import json
from datetime import datetime as dt

auth_url = 'https://classic.warcraftlogs.com/oauth/authorize'
token_url = 'https://classic.warcraftlogs.com/oauth/token'
config_path = '../wow_config.ini'
working_dir = os.getcwd()

# Get client, key, and secret from ini file
def get_credentials (auth_url, token_url, config_path):
    """Get client, key, and secret from ini file"""
    config = cp.ConfigParser()
    config.read(config_path)
    client_id = config.get('client', 'wowlogs')
    key = config.get('key', 'wowlogs')
    secret = config.get('secret', 'wowlogs')
    try:
        r = requests.post(token_url, 
            data={'grant_type': 'client_credentials'}, 
            auth=(client_id, secret))
        result = json.loads(r.text)
        return result, key, secret, client_id
    except:
        print('Connection Error')
        return 'Connection Error', key, secret, client_id
token, key, secret, client_id = get_credentials (auth_url, token_url, config_path)    

def format_name (name):
    """ Format any name for Wowlogs' API"""
    for i, s in enumerate(name):
        if i == 0:
            name = name.replace(name[i], name[i].upper())
        elif name[i] == ' ':
            try:
                if name[i+1:i+3] != 'of':
                    name = name.replace(name[i+1], name[i+1].upper())
            except:
                continue
    name = name.replace(' ', "%20")
    return name

def get_guild_reports (key, guild, server):
    """Fetch a list of raid logs"""
    url = 'https://classic.warcraftlogs.com:443/v1/reports/guild/' \
            + guild + '/' + server + '/US?api_key=' + key
    tmp = pd.DataFrame()
    try:
        r  = requests.get (url)
        result = json.loads(r.text)
        for r in result: # Saves the results to a dataframe
            r['end'] = dt.utcfromtimestamp(r['end']/1000).strftime('%Y-%m-%d')
            r['start'] = dt.utcfromtimestamp(r['start']/1000).strftime('%Y-%m-%d')
            tmp = tmp.append(r, ignore_index = True)
        return tmp
    except:
            print('Connection Error')
            return tmp

def get_report_fights (report):
    """Get the general data from each fight in a raid log"""
    url = 'https://classic.warcraftlogs.com:443/v1/report/fights/' + \
            report + '?api_key=' + key
    fights = pd.DataFrame()
    players = pd.DataFrame()
    enemies = pd.DataFrame()
    r = requests.get(url)
    result = json.loads(r.text)
    for fight in result['fights']:
        fight['time_to_kill'] = dt.utcfromtimestamp((fight['end_time'] - fight['start_time'])/1000).strftime('%HH:%MM:%SS')
        fight['start_time'] = dt.utcfromtimestamp(fight['start_time']/1000).strftime('%H:%M:%S')
        fight['end_time'] = dt.utcfromtimestamp(fight['end_time']/1000).strftime('%H:%M:%S')
        fights = fights.append(fight, ignore_index = True)
    for friend in result['friendlies']:
        players = players.append(friend, ignore_index = True)
    for enemy in result['enemies']:
        enemies = enemies.append(enemy, ignore_index = True) 
    players = players.drop('fights', axis = 1)
    enemies = enemies.drop('fights', axis = 1)
    fights.to_csv(os.path.join(working_dir,'data', report + '_fights.csv'), index = False)
    players.to_csv(os.path.join(working_dir,'data',report + '_players.csv'), index = False)
    enemies.to_csv(os.path.join(working_dir,'data',report + '_enemies.csv'), index = False)
    return fights, players.dropna(), enemies

def get_report_events(report, event):
    """Get detailed reports on group performance """
    tmp = pd.DataFrame()
    url = 'https://classic.warcraftlogs.com:443/v1/report/events/' + \
            event + '/' + report + '?api_key=' + key
    print(url)
    try:
        r = requests.get(url)
        result = json.loads(r.text)
        for res in result['events']:
            tmp = tmp.append(res, ignore_index = True)
        tmp.to_csv(os.path.join(working_dir,'data', report + '_' + event + '_.csv'), index = False)
        display(HTML('<hr><h4>' + event + '</h4>'))
        display(HTML(tmp.to_html()))
    except:
        print("Connection Error: Event = ", event)
    return tmp

#event_types = ['summary','damage-done','damage-taken', 'healing', 'casts', 
#            'summons', 'buffs', 'debuffs', 'deaths', 'threat', 'resources', 'interrupts', 'dispels']
#guild = format_name ('nerds of prey')
#server = format_name ('mankrik')

#reports = get_guild_reports (key, guild, server)
#fights, players, enemies = get_report_fights('VwrG1Y84ZPkNf69X')
#event_list = []
#for event in event_types:
#    event_list.append(get_report_events(reports.id[0], event))


