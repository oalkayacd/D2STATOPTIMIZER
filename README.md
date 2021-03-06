## General Info
- All damage numbers obtained using energy weapons.
- Reload speed calculations are performed using the Reload Sheet 2: Electric Boogaloo by Sereni#8012 inspired by twitter.com/VanHolden304's reload info spreadsheet.

## Reload Speed, What Stacks With What?
- In short, they all stack up to a point. The reload stat caps at 100, so you can stack everything that adds to the reload stat until you reach a reload stat of 100. RDS’s stack multiplicatively, so if you have Alloy Mag (REDS 0.85), Rapid-Fire Frame (REDS 0.8), and a regular loader (RDS 0.85), you would just multiply the RDS values together for a new RDS of 0.578 that you would apply to the reload. RDS’s technically don’t have a cap, but each weapon type has a unique reload speed cap. You can reach that reload cap by having a reload stat of 100 and applying a specific RDS to the weapon (I’ll tell you each individual reload cap when we start talking about weapon types), or you can hit the cap by having a very large RDS. -VanHolden

## RDS numbers modCheck?
- Reload Duration Scale (RDS) numbers currently in use are supplied from https://www.reddit.com/r/CruciblePlaybook/comments/igc6kq/massive_breakdown_of_reload_speed_including/. Any missing RDS's can be set manually in config, based on estimates. RDSCaps assume 100 handling. Assume 0.7 RDS cap for bows.

## Time for Ammo
- Time until the ammo count updates during the reload. Assume 0.9 for bows.

## Draw and Stow Speed
- Taken from u/Shrimp276s post https://www.reddit.com/r/DestinyTheGame/comments/od5irh/ever_wondered_how_handling_works_in_destiny/

## To-Do and Sidenotes:
- Using 1.1 crit modifier for pellet shotguns and 1.75 crit modifier for slugs across all enemy types.
- Currently using full auto config option only on aggressive and precision shotguns. 
- Rapid fire frame shotguns don't get assault mag, therefore the config has no effect.
- Shotguns use a separate number of reloads compared to other special weapons, since shotguns get reloaded one bullet at a time.
- Shotgun single reload assumes shotgun RoF > time for single reload
- Does rapid fire frame intrinsic affect fire rates?
- Check bow DPS correctness.