import json

replist = {}


def handle(name, guild, action, varname=None, data=None):
    if action == "add":
        o = checkInfo(name)
        if o == "Error":
            addEntry(name, guild)
            updateInfo(name, varname, data)
        else:
            updateInfo(name, varname, data)
    elif action == "check":
        o = checkInfo(name)
        if o == "Error":
            return "User doesnt exist in database"
        else:
            return o


def savetojson(dict):
    with open('varStorage.json', 'w') as fp:
        json.dump(dict, fp, indent=4)


def loadfromjson():
    try:
        with open('varStorage.json') as json_file:
            global replist
            replist = json.load(json_file)
    except json.decoder.JSONDecodeError:
        addEntry("Placeholder", 0, 0)


def updateInfo(name, varN, data):
    loadfromjson()
    if name in replist and varN is not None and data is not None:
        replist[name][varN] = data
        savetojson(replist)
    else:
        return "Error"


def toggle_info(name, varN):
    loadfromjson()
    if name in replist and varN in replist.get(name):
        replist[name][varN] = not replist[name][varN]
        savetojson(replist)
    else:
        return "Error"

def checkInfo(name):
    loadfromjson()
    try:
        return replist[name]
    except:
        return "Error"


def get_value(name, val):
    loadfromjson()
    try:
        return replist.get(name, {}).get(val)
    except:
        return "Error"


def addEntry(name, id, guild):
    replist[name] = {
        "memberID": id,
        "guildID": guild,
        "sentry_enabled": False
    }
    savetojson(replist)
    return "done"