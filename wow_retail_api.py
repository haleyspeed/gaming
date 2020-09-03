import requests
import json
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import os
import wget

def get_char_achievements(player, realm, row, access_token):
    "Retrieves achievements for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm \
          + '/' + player + '/achievements?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        return 'error'
    if r.status_code == 200:
        try:
            unpacked = json.loads(r.text)
            row['total_achievements'] = unpacked['total_quantity']
            row['total_achievement_points'] = unpacked['total_points']
            for achievement in unpacked['achievements']:
                try:
                    if achievement['criteria']['is_completed'] == True:
                        row[str(achievement['id'])] = datetime.datetime.utcfromtimestamp((int(achievement['completed_timestamp'])/1000)).strftime('%Y-%m-%d')
                    else:
                        row[str(achievement['id'])] = 'none'
                except:
                    row[str(achievement['id'])] = 'none'
            return row
        except:
            return 'error'
    else:
        return 'error'

def get_access_token (blizzard_key, blizzard_secret):
    """Get access token to access the blizzard API"""
    r = requests.post('https://us.battle.net/oauth/token', data={'grant_type': 'client_credentials'},
                  auth=(blizzard_key, blizzard_secret))
    unpacked = json.load(r.text)
    access_token = unpacked['access_token']
    return access_token

def get_player_achievements(player,realm, row, access_token):
    "Retrieves achievements for a player using the Blizzard API"
    url = 'https://us.api.blizzard.com/profile/wow/character/' + realm \
          + '/' + player + '/achievements?namespace=profile-us&locale=en_US&access_token=' + access_token
    try:
        r = requests.get(url)
    except:
        return 'error'
    if r.status_code == 200:
        try:
            unpacked = unpack_json(r.text)
            row['total_achievements'] = unpacked['total_quantity']
            row['total_achievement_points'] = unpacked['total_points']
            for achievement in unpacked['achievements']:
                try:
                    if achievement['criteria']['is_completed'] == True:
                        row[str(achievement['id'])] = datetime.datetime.utcfromtimestamp((int(achievement['completed_timestamp'])/1000)).strftime('%Y-%m-%d')
                    else:
                        row[str(achievement['id'])] = 'none'
                except:
                    row[str(achievement['id'])] = 'none'
            return row
        except:
            return 'error'
    else:
        return 'error'
