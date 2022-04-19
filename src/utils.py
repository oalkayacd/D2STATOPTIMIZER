import json

def readJSON(filepath):
    with open(filepath, 'r') as f:
        wep_data = json.load(f)
    return wep_data    

def calcReload(a, b, c, x):
    return ((a*(x**2)) + (b*x) + c)

def timeToEmptyOneMag(magsize, firerate, weapon_type): #firerate used for rpm for fully auto, draw time for bow, charge time for fusion and LFR
    # Special case weapons
    if(weapon_type == "Bow"):
        return firerate/1000
    # Add further special cases here...

    # Default case for fully automatic weapons without draw / charge time
    else:
        return (magsize-1)/(firerate/60) #magsize-1 because first shot is fired instantly
