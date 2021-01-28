import json
import os

replist = {}


def handle(name, guild, action, varname=None, data=None):
    if action == "add":
        o = check_info(name)
        if o == "Error":
            add_entry(name, guild)
            update_info(name, varname, data)
        else:
            update_info(name, varname, data)
    elif action == "check":
        o = check_info(name)
        if o == "Error":
            return "User doesnt exist in database"
        else:
            return o


def save_to_json(dict):
    with open('varStorage.json', 'w') as fp:
        json.dump(dict, fp, indent=4)


def load_from_json():
    try:
        with open('varStorage.json') as json_file:
            global replist
            replist = json.load(json_file)
    except json.decoder.JSONDecodeError:
        add_entry("Placeholder", 0, 0)


def update_info(name, varN, data):
    load_from_json()
    if name in replist and varN is not None and data is not None:
        replist[name][varN] = data
        save_to_json(replist)
    else:
        return "Error"


def toggle_info(name, varN):
    load_from_json()
    if name in replist and varN in replist.get(name):
        replist[name][varN] = not replist[name][varN]
        save_to_json(replist)
    else:
        return "Error"

def check_info(name):
    load_from_json()
    try:
        return replist[name]
    except:
        return "Error"


def get_value(name, val):
    load_from_json()
    try:
        return replist.get(name, {}).get(val)
    except:
        return "Error"


def add_entry(name, id, guild):
    replist[name] = {
        "memberID": id,
        "guildID": guild,
        "sentry_enabled": False
    }
    save_to_json(replist)
    return "done"