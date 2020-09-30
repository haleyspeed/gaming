import os
import configparser
import requests
import datetime
import json
import numpy as np
import pandas as pd
from IPython.display import HTML,display

# Use Configparser to read in protected data from an external config.ini file
app_id = 440
dir_in = "//Users//haleyspeed//Docs//insight//api"
f_config = 'config.ini'
config = configparser.ConfigParser()
os.chdir(dir_in)
config.read(f_config)
steam_key = config.get('KEYS', 'steam')
steam_id = config.get('ID', 'demo_steam_id')


# Fetch JSON data from steam's Web API
def get_steam_game_news (app_id):
    url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + str(app_id) + '&format=json'
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_steam_global_achievement_progress (app_id):
    url = 'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=' + str(app_id) + '&format=json'
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_steam_global_game_stats (app_id):
    url = 'http://api.steampowered.com/ISteamUserStats/GetGlobalStatsForGame/v0001/?format=json&appid=' + str(app_id) + '&count=1&name%5B0%5D=global.map.emp_isle'
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_player_summaries (steam_key, steam_id):
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + str(steam_key) + '&steamids=' + str(steam_id)
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_player_friends (steam_key, steam_id):
    url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + str(steam_key) + '&steamid=' + str(steam_id) + '&relationship=friend'
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_player_achievements (app_id,steam_key, steam_id):
    url = 'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=' + str(app_id) + '&key=' + str(steam_key) + '&steamid=' + str(steam_id)
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_user_stats_per_game (app_id,steam_key,steam_id):
    url = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid='+ str(app_id) + '&key=' + str(steam_key) + '&steamid=' + str(steam_id)
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_recently_played_games (steam_key,steam_id):
    url = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=' + str(steam_key) + '&steamid=' + str(steam_id) + '&format=json'
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_shared_games (steam_key,steam_id):
    url = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=' + str(steam_key) + '&steamid=' + str(steam_id) + '&format=json'
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_game_schema (app_id, steam_key):
    url = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=' + str(steam_key)+ '&appid= '+ str(app_id)
    r = requests.get(url, data = {'key':'value'})
    return r.text


def get_player_bans (app_id, steam_key):
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=' + str(steam_key)+ '&steamids='+ str(steam_id)
    r = requests.get(url, data = {'key':'value'})
    return r.text


# Format JSON data for analysis in Python
def unpack_json(txt):
    unpacked = json.loads(txt)
    return unpacked


def explore_game_news(unpacked):
    df = pd.DataFrame()
    for keys, appnews in unpacked.items():
        for keys, news_items in appnews.items():
            if keys == 'appid':
                row = [keys]
            if keys == 'newsitems':
                for item in news_items:
                    df = df.append(item, ignore_index=True)
    # display(HTML(df.head().to_html()))  # For testing. Outputs a huge table
    return df


def display_news(news):
    """Outputs latest news for a specific game in HTML format, including
    images and embedded videos"""
    for i, title in enumerate(news.title):
        display(HTML('<h1>' + title + '</h1>' +
                     '<br><strong>Author: </strong>' + news.author[i] + '<br>' +
                     '<strong>App ID: </strong>' + str(news.appid[i]) + '<br>' +
                     '<strong>Date: </strong>' + str(datetime.datetime.utcfromtimestamp(news.date[i],datetime.timezone.utc)) + '<br>' +
                     '<strong>ID: </strong>' + str(news.gid[i]) + '<br>' +
                     '<strong>URL: </strong>' + str(news.url[i]) + '<br>' +
                     '<strong>Feed Label: </strong>' + str(news.feedlabel[i]) + '<br>' +
                     '<strong>Feed Name: </strong>' + str(news.feedname[i]) + '<br>' +
                     '<strong>Feed Type: </strong>' + str(news.feed_type[i]) + '<br>'))
        display(HTML(
            '<br>' + news.contents[i].replace('[', '<').replace(']', '>').replace('<*>', '<br>* ').replace('<h1>',
                                                                                                           '<h3>').replace(
                '</h1>', '</h3>') + '<hr><br>'))


def explore_global_achievements(unpacked):
    df = pd.DataFrame(columns=['achievement', 'percent'])
    name = ''
    percent = np.nan
    for keys, achievementpercentages in unpacked.items():
        for keys, achievements in achievementpercentages.items():
            for i, achievement in enumerate(achievements):
                for keys, names_percent in achievement.items():
                    if isinstance(names_percent, str) == True:
                        name = names_percent
                    if isinstance(names_percent, float) == True or isinstance(names_percent, int):
                        percent = names_percent
                        df = df.append({"achievement": name, "percent": percent}, ignore_index=True)

    display(HTML(df.head().to_html()))
    return df


def explore_steam_global_stats(unpacked):
    df = pd.DataFrame()
    for keys, response in unpacked.items():
        for keys, values in response.items():
            if isinstance(values, dict):
                for keys, results in values.items():
                    tmp = pd.DataFrame()
                    for keys, more_results in results.items():
                        tmp[keys] = [more_results]
                    df = df.append(tmp)
            else:
                df[keys] = [values]

    display(HTML(df.head().to_html()))
    return df


def explore_player_summaries (unpacked):
    df = pd.DataFrame ()
    for keys,response in unpacked.items():
        for keys,players in response.items():
            for player in players:
                tmp = pd.DataFrame()
                for keys,values in player.items():
                    tmp[keys] = [values]
                df = df.append(tmp)
    df = df.transpose()
    display(HTML(df.head().to_html()))
    return df


def explore_player_friends (unpacked):
    df = pd.DataFrame ()
    for keys, friendslist in unpacked.items():
        for keys, friends in friendslist.items():
            for friend in friends:
                tmp = pd.DataFrame()
                for keys, values in friend.items():
                    if "friend_since" in keys:
                        values =  datetime.datetime.fromtimestamp(values, datetime.timezone.utc)
                    tmp[keys] = [values]
                df = df.append(tmp)
    display(HTML(df.head().to_html()))
    return df


def explore_player_achievements(unpack):
    df = pd.DataFrame ()
    for keys, playerstats in unpack.items():
        for keys,steam_id in playerstats.items():
            if 'error' in keys:
                print('Profile is not public')
            else:
                if "achievements" in keys:
                    for achievements in steam_id:
                        tmp = pd.DataFrame()
                        for keys, values in achievements.items():
                            if 'unlocktime' in keys:
                                values = datetime.datetime.utcfromtimestamp(values,datetime.datetime.utc)
                            tmp[keys] = [values]
                        df = df.append(tmp)
    display(HTML(df.head().to_html()))
    return df


def explore_recent_games (unpacked):
    df = pd.DataFrame ()
    for keys,values in unpacked.items():
        for key, games in values.items():
            if 'games' in key:
                for game in games:
                    tmp = pd.DataFrame()
                    for key, item in game.items():
                        tmp [key] = [item]
                    df = df.append(tmp)
    display(HTML(df.head().to_html()))
    return df


def explore_shared_games (unpacked):
    df = pd.DataFrame ()
    for keys,values in unpacked.items():
        for keys, total_count in values.items():
            if isinstance(total_count, list):
                tmp = pd.DataFrame()
                for count in total_count:
                    for key, value in count.items():
                        tmp[key] = [value]
                    df = df.append(tmp)
    display(HTML(df.head().to_html()))
    return df


def explore_game_schema (unpacked):
    df = pd.DataFrame ()
    gameName = ''
    gameVersion = np.nan
    for keys,game in unpacked.items():
        i = 0
        for field, subfield in game.items():
            if field == 'gameName':
                gameName = subfield
            elif field == 'gameVersion':
                gameVersion = subfield
            elif field == 'availableGameStats':
                tmp = pd.DataFrame()
                for keys,values in subfield.items():
                    for value in values:
                        for keys, schema in value.items():
                            tmp[keys] = [schema]
                            tmp['gameName'] = gameName
                            tmp['gameVersion'] = gameVersion
                        df = df.append(tmp)
    display(HTML(df.head().to_html()))
    return df


def explore_player_bans(unpacked):
    df = pd.DataFrame()
    for keys, values in unpacked.items():
        for key, value in values[0].items():
            df[key] = [value]
    display(HTML(df.head().to_html()))
    return df


