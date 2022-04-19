import json

def readJSON(filepath):
    with open(filepath, 'r') as f:
        wep_data = json.load(f)
    return wep_data    

def calcReload(a, b, c, x):
    return ((a*(x^2)) + (b*x) + c)
