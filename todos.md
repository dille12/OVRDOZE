## List of tasks or improvements to be made.

here is a way to organize future features, and coordinate work on the game.
or for new people who want to help: here are things that still need to get done.

# Important
1. Begin unit testing.
2. Begin automatic testing pipeline in github.

# Road to 1.0

## Content
1. 3-5 more levels.
2. Finish soldier class, a harder gun wielding enemy present in some levels.
3. A boss in last level.
4. Explosive weapons and couple more energy weapons.
5. More stuff to do in overworld. Stock market, upgrades for you and the robot, bigger inventory purchases.
6. More dialogue (more NPCs).
7. More equipment (a temporary radar consumable, which reveals a Halo-like radar in HUD).
8. ~~Separate "career" mode from endless mode, start a career mode by starting game in Overworld.~~
9. Ability to save progress in career mode.
10. Add a thank you page for collaborators.
11. A zombie that chucks explosive fleshbombs.

## Multiplayer
1. Synchronize:
  * Item drops
    - When someone picks the item up, the item disappears.
    - When a zombie or player drops something, the items will be transferred to other players.
  * Lootboxes
    - Items are synchronized and when you manipulate the inventory other players will get that information
  * Zombies
    - Make that zombies follow the closest player that they spawn to.
    - The one that the zombie follows computes the zombies movement.
    - Send info about the zombies.
    - Ability for the zombies to change target based on distance or visibility.
    - Packets shouldn't be sent every tick, so figure out a sustainable way to keep up.
  * Turrets
    - Turrets will shoot anything that isn't their owner on PvP, or just zombies.
    - Turrets will be computed on their owners' computers.

  * Moving turret
    - Scrapped for now.

  * Wave times and enemy count
    - Overhaul the whole system
    - Serverside timer?
      * When the first player enters the level, a packet will be sent which contains the order for the server to start the wave timer. When the timer reaches certain points, it will send the order to toggle the wave.
    - Enemy count should be derived from wave number rather than time spent on the level.
    - Sanity will remain, each player contributes to the amount of the zombies.
  * Players
    - Melee

2. PvP Gamemodes:
  - I.E Multiple capture points in level, that need to be captured and protected.
  - Deathmatch
  - Gun Game
  - More maps like Downtown

3. Career mode
  - Players will only be computed if they are on the same level.
  - Shared money?

## Known bugs
1. ~~Quitting to main menu and starting overworld again doesn't reset the map.~~
2. HUD displacement in higher resolutions.
3. ~~Knockback is not affected by fps timedelta.~~
4. ~~On higher resolutions zombies grind the game to a halt. Figure out what causes this (not the rendering!)~~
5. ~~Investigate why zombies get stuck in Requiem in lower right corner.~~
