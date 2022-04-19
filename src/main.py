import py_compile
import sys
from utils import readJSON, readConfig

def main():
    config = readConfig()
    legendary_weapon_data = readJSON(config.get('Paths', 'LegendaryWeaponPath')).get('Weapons')
    primary_weapon_data =   legendary_weapon_data.get('Primary')
    sidearm_data =          primary_weapon_data.get('Sidearm')
    smg_data =              primary_weapon_data.get('SMG')
    autorifle_data =        primary_weapon_data.get('Auto Rifle')
    pulserifle_data =       primary_weapon_data.get('Pulse Rifle')
    scoutrifle_data =       primary_weapon_data.get('Scout Rifle')
    handcannon_data =       primary_weapon_data.get('Hand Cannon')
    bow_data =              primary_weapon_data.get('Bow')

    




    return 0

if __name__ == '__main__':
    sys.exit(main())    