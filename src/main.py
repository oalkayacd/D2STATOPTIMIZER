import py_compile
import sys
from utils import readJSON, readConfig

def main():
    config = readConfig()
    legendary_weapon_data = readJSON(config.get('Paths', 'LegendaryWeaponPath')).get('Weapons')
    primary_weapon_data = legendary_weapon_data.get('Primary')
    scout_data = primary_weapon_data.get('Scout Rifle')
    autorifle_data = primary_weapon_data.get('Auto Rifle')
    pulse_data = primary_weapon_data.get('Pulse Rifle')
    scout_data = primary_weapon_data.get('Scout Rifle')
    scout_data = primary_weapon_data.get('Scout Rifle')
    scout_data = primary_weapon_data.get('Scout Rifle')




    return 0

if __name__ == '__main__':
    sys.exit(main())    