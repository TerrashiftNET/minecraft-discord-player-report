#!/usr/bin/env python3
''' Script used to report last minecraft player login times '''

import json
import os
import datetime
from tabulate import tabulate
from dhooks import Webhook, Embed


def modification_date(filename):
    ''' Check last playerdata modification date '''
    if os.path.exists(filename):
        unix_time = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(unix_time).strftime('%m-%d')
    return "none"


def load_whitelist(whitelist_file):
    ''' load whitelist.json as a dictionary'''
    with open(whitelist_file) as whitelist:
        whitelist_dict = json.load(whitelist)
    return whitelist_dict


def get_login_info(whitelist_dict, player_stat_location):
    ''' get user:last_logged_in information from stats '''
    playerdata_dict = {}
    for playerdata in whitelist_dict:
        playerfile = player_stat_location + playerdata['uuid'] + ".json"
        last_logged_in = modification_date(playerfile)
        playerdata_dict[playerdata['name']] = last_logged_in
    return playerdata_dict


def sort_payload(playerdata):
    ''' sort playerdata_dict by date and prepare for discord webhook '''
    payload = dict(sorted(playerdata.items(), key=lambda p: p[1], reverse=True))
    return payload


def prepare_payload(payload):
    ''' Create a table out of sorted player data '''
    table = (payload.items())
    table = tabulate(table, headers=["Player", "Last seen"], tablefmt="github")
    table = ''.join(('```\n', table, '\n```'))
    return table


def send_report(payload, hook_url):
    '''create embed with info from prepared payload and send via discord webhook'''
    today = datetime.date.today().strftime("%Y-%m-%d")
    embed = Embed(
        title="Player activity report for {}".format(today),
        description=payload,
        color=0x5CDBF0,)

    hook = Webhook(hook_url)
    hook.send(embed=embed)


if __name__ == '__main__':
    with open("config.json") as f:
        config = json.loads(f.read())

    WHITELIST_FILE = config["whitelist"]
    PLAYER_STAT_LOCATION = config["stat_location"]
    WEBHOOK_URL = config["webhook_url"]


    whitelist_dictionary = load_whitelist(WHITELIST_FILE)
    player_login_data = get_login_info(whitelist_dictionary, PLAYER_STAT_LOCATION)
    DISCORD_PAYLOAD = prepare_payload(sort_payload(player_login_data))
    send_report(DISCORD_PAYLOAD, WEBHOOK_URL)
