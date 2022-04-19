from imp import reload
import sys
from utils import readJSON, calcReload
from configparser import ConfigParser

def main():
    # Read Config
    config = ConfigParser()
    config.read('src/config.cfg')

    # Read JSON
    legendary_weapon_damage_data = readJSON(config.get('Paths', 'LegendaryWeaponPath')).get('Weapons')
    reload_data = readJSON(config.get('Paths', 'ReloadSpeedPath'))

    # Get reload stat and assert range
    reload_stat = int(config.get('Options', 'ReloadStat'))
    assert 0 <= reload_stat and reload_stat <= 100, 'Base Reload Stat not in range 0-100'
    # Read default estimate value for RDScap
    DefaultCapRDS = float(config.get('Options', 'DefaultCapRDS'))
    AppliedRDS = float(config.get('Options', 'AppliedRDS'))

    # reload_stat < 10 does not affect animation speed
    if(reload_stat < 10):
        reload_stat = 10

    # Primary Weapons
    # Iterate through weapon types
    for weapon_type in legendary_weapon_damage_data.get('Primary'):
        archetypes = legendary_weapon_damage_data['Primary'][weapon_type]['Archetypes']

        # Get reload for weapon type
        reload_a = reload_data['Primary'][weapon_type].get('a')
        reload_b = reload_data['Primary'][weapon_type].get('b')
        reload_c = reload_data['Primary'][weapon_type].get('c')
        RDSCap = reload_data['Primary'][weapon_type].get('RDScap')

        # Check for missing RDSCap values, use default from config if none found
        if(RDSCap == None):
            RDSCap = DefaultCapRDS

        # Calculate reload and cap the reload speed up to 100 reload stat with RDSCap
        reload_in_s = calcReload(reload_a, reload_b, reload_c, reload_stat) * AppliedRDS
        reload_cap_in_s =  calcReload(reload_a, reload_b, reload_c, 100) * RDSCap
        reload_in_s = max(reload_in_s, reload_cap_in_s)
        

        # Iterate through weapon archetypes within a type
        for archetype in archetypes:
            table_row = []

            # Add weapon type and archetype
            table_row.append(weapon_type)
            table_row.append(archetype.get('Archetype'))

            # Get firerate and append
            firerate = archetype.get('Firerate')
            table_row.append(str(firerate))

            # Get damage numbers
            boss_body   = archetype.get('Boss Bodyshot Damage')
            major_body  = archetype.get('Major Bodyshot Damage')
            minor_body  = archetype.get('Minor Bodyshot Damage')
            minor_head  = archetype.get('Minor Headshot Damage')

            # Headshot mult
            hs_mult = minor_head / minor_body 
            table_row.append(str(hs_mult))

            # Get remaining headshot numbers
            boss_head   = boss_body * hs_mult
            major_head  = major_body * hs_mult

            # Add bodyshot and headshot numbers for minor, major, boss
            table_row.append(str(minor_body))
            table_row.append(str(minor_head))
            table_row.append(str(major_body))
            table_row.append(str(major_head))
            table_row.append(str(boss_body))
            table_row.append(str(boss_head))
            table_row.append(str(reload_in_s))
            table_row.append(str(reload_cap_in_s))

            print(table_row)
            

            

    
    return 0

if __name__ == '__main__':
    sys.exit(main())