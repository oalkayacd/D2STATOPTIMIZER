import sys
from utils import readJSON, calcReload, timeToEmptyOneMag
from configparser import ConfigParser
import pandas as pd

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

    # Read applied RDS
    AppliedRDS = float(config.get('Options', 'AppliedRDS'))

    # Read number of reloads performed to obtain average DPS for primaries
    NumOfPrimaryReloads = int(config.get('Options', 'NumOfPrimaryReloads'))

    # Read number of reloads performed to obtain average DPS for specials
    NumOfSpecialReloads = int(config.get('Options', 'NumOfSpecialReloads'))

    # reload_stat < 10 does not affect animation speed (check if this still holds in S17)
    if(reload_stat < 10):
        reload_stat = 10

    # Primary Weapons
    # Store final primary weapon data as a 2d list
    primary_table = []

    # Iterate through weapon types
    for weapon_type in legendary_weapon_damage_data.get('Primary'):
        archetypes = legendary_weapon_damage_data['Primary'][weapon_type]['Archetypes']

        # Get reload for weapon type
        reload_a = reload_data['Primary'][weapon_type].get('a')
        reload_b = reload_data['Primary'][weapon_type].get('b')
        reload_c = reload_data['Primary'][weapon_type].get('c')
        RDSCap = reload_data['Primary'][weapon_type].get('RDScap')
        TimeForAmmo = reload_data['Primary'][weapon_type].get('TimeForAmmo')

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

            # Get firerate / draw speed and append
            firerate = archetype.get('Firerate')
            drawtime = archetype.get('DrawTime')
            if(weapon_type == "Bow"):
                table_row.append(str(drawtime)+ " ms")
                firerate = drawtime # for further use in timeToEmptyOneMag
            else:
                table_row.append(str(firerate)+ " rpm")    

            # Get damage numbers
            boss_body   = archetype.get('Boss Bodyshot Damage')
            major_body  = archetype.get('Major Bodyshot Damage')
            minor_body  = archetype.get('Minor Bodyshot Damage')
            minor_head  = archetype.get('Minor Headshot Damage')
            magsize = archetype.get('Magsize')

            # Headshot mult
            hs_mult = minor_head / minor_body 
            table_row.append(str("%.3f" % round(hs_mult, 3)))

            # Get remaining headshot numbers
            boss_head   = boss_body * hs_mult
            major_head  = major_body * hs_mult

            # Add bodyshot and headshot numbers for minor, major, boss
            table_row.append(str("%.2f" % round(minor_body, 2)))
            table_row.append(str("%.2f" % round(minor_head, 2)))
            table_row.append(str("%.2f" % round(major_body, 2)))
            table_row.append(str("%.2f" % round(major_head, 2)))
            table_row.append(str("%.2f" % round(boss_body, 2)))
            table_row.append(str("%.2f" % round(boss_head, 2)))

            # Add reload, reload cap, time for ammo, time for ammo cap
            table_row.append(str("%.2f" % round(reload_in_s, 2)))
            table_row.append(str("%.2f" % round(reload_cap_in_s, 2)))
            table_row.append(str("%.2f" % round(reload_in_s * TimeForAmmo, 2)))
            table_row.append(str("%.2f" % round(reload_cap_in_s * TimeForAmmo, 2))) 

            # Time to empty 1 mag
            one_mag_time = timeToEmptyOneMag(magsize, firerate, weapon_type)  # firerate = drawrate for bows
            table_row.append(str("%.2f" % round(one_mag_time, 2)))

            # One mag headshot dmg for minor, major, boss
            one_mag_minor_head_dmg = magsize * minor_head
            one_mag_major_head_dmg = magsize * major_head
            one_mag_boss_head_dmg  = magsize * boss_head
            table_row.append(str("%.1f" % round(one_mag_minor_head_dmg, 1)))
            table_row.append(str("%.1f" % round(one_mag_major_head_dmg, 1)))
            table_row.append(str("%.1f" % round(one_mag_boss_head_dmg, 1)))

            # One mag headshot dps for minor, major, boss
            table_row.append(str("%.1f" % round(one_mag_minor_head_dmg / one_mag_time, 1)))
            table_row.append(str("%.1f" % round(one_mag_major_head_dmg / one_mag_time, 1)))
            table_row.append(str("%.1f" % round(one_mag_boss_head_dmg / one_mag_time, 1)))

            # Average DPS over reloads for minor, major, boss
            avg_time = (NumOfPrimaryReloads * reload_in_s) + ((NumOfPrimaryReloads + 1) * one_mag_time)
            table_row.append(str("%.1f" % round(((NumOfPrimaryReloads + 1) * one_mag_minor_head_dmg) / avg_time, 1)))
            table_row.append(str("%.1f" % round(((NumOfPrimaryReloads + 1) * one_mag_major_head_dmg) / avg_time, 1)))
            table_row.append(str("%.1f" % round(((NumOfPrimaryReloads + 1) * one_mag_boss_head_dmg)  / avg_time, 1)))
            primary_table.append(table_row)
            print(table_row)

    primary_df = pd.DataFrame(primary_table)
    primary_df.to_csv('data/csv/primary_weapons.csv', header=["Weapon Type","Weapon Archetype","RPM / Draw Time/ Charge Time","HS Multiplier", "Minor Body" , "Minor Head", "Major Body" , "Major Head", "Boss Body" , "Boss Head", "Reload Speed", "Reload Speed Cap", "Time For Ammo", "Time For Ammo Cap", "Time To Empty 1-Mag", "1-Mag Minor HS DMG", "1-Mag Major HS DMG", "1-Mag Boss HS DMG", "1-Mag Minor HS DPS", "1-Mag Major HS DPS", "1-Mag Boss HS DPS", "Avg Minor HS DPS", "Avg Major HS DPS", "Avg Boss HS DPS"])
            
    # Special Weapons
    # Store final Special data as a 2d list
    special_table = []        

    # Iterate through weapon types
    for weapon_type in legendary_weapon_damage_data.get('Special'):
        archetypes = legendary_weapon_damage_data['Special'][weapon_type]['Archetypes']

        # Get reload for weapon type
        reload_a = reload_data['Special'][weapon_type].get('a')
        reload_b = reload_data['Special'][weapon_type].get('b')
        reload_c = reload_data['Special'][weapon_type].get('c')
        RDSCap = reload_data['Special'][weapon_type].get('RDScap')
        TimeForAmmo = reload_data['Special'][weapon_type].get('TimeForAmmo')

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

            # Get firerate and consider config options for shotguns
            firerate = archetype.get('Firerate')

            if(weapon_type == "Shotgun"):
                if(int(config.get('Options', 'AssaultMag'))):
                    if (archetype == "Lightweight"):
                        firerate = firerate + 10
                    else:
                        firerate = firerate + 5    
                if(int(config.get('Options', 'FullAuto'))) :
                    firerate = firerate * 1.1   

            table_row.append(str(firerate)+ " rpm")    

            # Get damage numbers
            boss_body   = archetype.get('Boss Bodyshot Damage')
            major_body  = archetype.get('Major Bodyshot Damage')
            minor_body  = archetype.get('Minor Bodyshot Damage')
            minor_head  = archetype.get('Minor Headshot Damage')
            magsize = archetype.get('Magsize')

            # Headshot mult
            hs_mult = minor_head / minor_body 
            table_row.append(str("%.3f" % round(hs_mult, 3)))

            # Get remaining headshot numbers
            boss_head   = boss_body * hs_mult
            major_head  = major_body * hs_mult

            # Add bodyshot and headshot numbers for minor, major, boss
            table_row.append(str("%.2f" % round(minor_body, 2)))
            table_row.append(str("%.2f" % round(minor_head, 2)))
            table_row.append(str("%.2f" % round(major_body, 2)))
            table_row.append(str("%.2f" % round(major_head, 2)))
            table_row.append(str("%.2f" % round(boss_body, 2)))
            table_row.append(str("%.2f" % round(boss_head, 2)))

            # Add reload, reload cap, time for ammo, time for ammo cap
            table_row.append(str("%.2f" % round(reload_in_s, 2)))
            table_row.append(str("%.2f" % round(reload_cap_in_s, 2)))
            table_row.append(str("%.2f" % round(reload_in_s * TimeForAmmo, 2)))
            table_row.append(str("%.2f" % round(reload_cap_in_s * TimeForAmmo, 2))) 

            # Time to empty 1 mag
            one_mag_time = timeToEmptyOneMag(magsize, firerate, weapon_type)  # firerate = drawrate for bows
            table_row.append(str("%.2f" % round(one_mag_time, 2)))

            # One mag headshot dmg for minor, major, boss
            one_mag_minor_head_dmg = magsize * minor_head
            one_mag_major_head_dmg = magsize * major_head
            one_mag_boss_head_dmg  = magsize * boss_head
            table_row.append(str("%.1f" % round(one_mag_minor_head_dmg, 1)))
            table_row.append(str("%.1f" % round(one_mag_major_head_dmg, 1)))
            table_row.append(str("%.1f" % round(one_mag_boss_head_dmg, 1)))

            # One mag headshot dps for minor, major, boss
            table_row.append(str("%.1f" % round(one_mag_minor_head_dmg / one_mag_time, 1)))
            table_row.append(str("%.1f" % round(one_mag_major_head_dmg / one_mag_time, 1)))
            table_row.append(str("%.1f" % round(one_mag_boss_head_dmg / one_mag_time, 1)))

            # Average DPS over reloads for minor, major, boss
            avg_time = (NumOfSpecialReloads * reload_in_s) + ((NumOfSpecialReloads + 1) * one_mag_time)
            table_row.append(str("%.1f" % round(((NumOfSpecialReloads + 1) * one_mag_minor_head_dmg) / avg_time, 1)))
            table_row.append(str("%.1f" % round(((NumOfSpecialReloads + 1) * one_mag_major_head_dmg) / avg_time, 1)))
            table_row.append(str("%.1f" % round(((NumOfSpecialReloads + 1) * one_mag_boss_head_dmg)  / avg_time, 1)))
            special_table.append(table_row)
            print(table_row)

    special_df = pd.DataFrame(special_table)
    special_df.to_csv('data/csv/special_weapons.csv', header=["Weapon Type","Weapon Archetype","RPM / Draw Time/ Charge Time","HS Multiplier", "Minor Body" , "Minor Head", "Major Body" , "Major Head", "Boss Body" , "Boss Head", "Reload Speed", "Reload Speed Cap", "Time For Ammo", "Time For Ammo Cap", "Time To Empty 1-Mag", "1-Mag Minor HS DMG", "1-Mag Major HS DMG", "1-Mag Boss HS DMG", "1-Mag Minor HS DPS", "1-Mag Major HS DPS", "1-Mag Boss HS DPS", "Avg Minor HS DPS", "Avg Major HS DPS", "Avg Boss HS DPS"])

    
    return 0

if __name__ == '__main__':
    sys.exit(main())