## List of tasks or improvements to be made.

here is a way to organize future features, and coordinate work on the game.
or for new people who want to help: here are things that still need to get done.
* [Important](#important) 
* [Easy](#easy-to-dos) 
* [If there's time](#if-theres-time)
* [Megahard changes](#megahard-changes)

# Important
1. Begin unit testing.
2. Begin automatic testing pipeline in github.

# Easy To-Dos

## general
1. ~~Impliment a way back to the menu screen from the game. (esc currently just closes the whole program)~~
3. Resolution: ability to change window size in game.
4. ~~Correct resolution detection of monitor.~~
5. In-game settings menu (volume / quit to menu / resolution)

### creative / artwork
1. Fire animations, molotovs and flamers
2. More and better OST
3. Animate the player sprite
4. Laser/Explosive weapons
5. More/Bigger maps
6. More items (body shields, decoys, radars) (also mechanics)
7. Ingame map editor 

### mechanics / gameplay
1. More zombie types (~~bombers~~, runners, rangers)
2. Last stand and reviving
3. More items (body shields, decoys, radars) (also art)
4. Sanity rework (currently only increases amount of zombies)
5. Melee combat system
6. ~~Right clicking on ammo from a box should automatically add it to inventory~~ Shift clicking quicktransfers items from boxes

### systems / networking / multiplayer
1. Correct IP scanning
2. PvE Multiplayer, ping counteracting
3. Figure out port-forwarding to access multiplayer.

### Efficencies and Optimizations
1. func.get_route() overhaul
2. los.render_los_image() line of sight fixes and optimization


# If there's time:
1. Small campaign
- Trigger system for maps
- Dialogue

# Megahard changes:

1. Changing the rendering resolution (it's capped to 854x480) 
2. Ability to change fps cap (Everything is tied to 60fps)
3. Procedural map generation
