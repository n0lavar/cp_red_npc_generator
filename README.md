# Cyberpunk Red NPC generator

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

<a href="https://buymeacoffee.com/n0lavar" target="_blank" title="buymeacoffee">
  <img src="https://iili.io/JIYMmUN.gif"  alt="buymeacoffee-animated-badge" style="width: 160px;">
</a>

## Info

A generator that generates NPCs based on json configs using the specified rank and role.  
See `configs/ranks.xlsl` for balance details.

Generated:

* Stats

  Stats are generated based on the list of stats for each role for a street rat from the rulebook: a random set is
  selected and scaled according to the rank. The lowest rank has a stat sum of 30, the highest has a stat sum of 80.


* Skills

  Skills are generated based on the list of skills for the role for a street rat from the rulebook: the list is taken
  and scaled according to rank. The lowest rank has a skill sum of 35, the highest has a skill sum of 115.

  Science and Martial Arts skills are generated without clarification, the user has to choose the required one
  themselves.


* Cyberware

  Cyberware is generated based on a list of cyberware unique to each role and a purchase budget that is determined by
  rank. The generator will attempt to buy dependent cyberware and paired cyberware. If a cyberware has modifiers, they
  will be added to stats/skills.


* Armor

  If armor or shields are generated in cyberware, they will be added. Otherwise, the generator will try to buy armor
  according to the maximum SP specified for the role. For example, media will be satisfied with Kevlar, while solo will
  try to buy Metalgear. If the budget is not enough, the generator will try to buy a cheaper armor. A body armor is
  generated with priority.


* Weapon

  If a weapon was generated in the cyberware, it will be added. If there was no weapon preferred by the role among these
  cyberware, it will be generated according to the budget. The main weapon will be generated with priority.

  All long-range weapons are generated unloaded, the user must select the required ammunition, subtract the amount of
  ammunition in the inventory and insert it into the weapon.

* Ammunition for selected weapons and grenades

  Some amount of basic ammunition will always be added. Further grenades and improved ammunition will be added according
  to role preference as long as there is enough money.


* Equipment

  Different tools will be generated that best suit the selected role. The tools will not replicate cyberware with
  similar functionality.


* Drugs

  If Airhypo was generated in the equipment, drugs will be generated that depend on the role of the NPC. For example, a
  solo will prefer Berserker, a netrunner - Sixgun, and a rockerboy will prefer Prime Time.


* Different junk for the entourage

  Various items that have no practical use and are intended to add realism to the contents of pockets. Some of them can
  be used by gamemaster for spontaneous stories (photo, letter, corporate business card), hiding places (key to safe,
  note). Most of them are worthless, but expensive items like a gold chain can be found.

## Usage

You may be a netrunner and not need such explanations, but not everyone here knows their way around a computer, choom!  
This is a console application, which means that you need to do the following to get a sensible result:

1. On the right side of the github page there is a releases section, open the last one.
2. Download `cp_red_npc_generator.zip`, unzip it anywhere you want.
3. Open Explorer where the `cp_red_npc_generator.exe` file is, type "cmd" in the address bar and press Enter.
4. Now you should see a command prompt opened in the right directory where you can type commands from examples.  
   Try this for starters: `cp_red_npc_generator.exe --rank=captain --role=solo`.

Here is the full list of available arguments and their explanation. Calling `cp_red_npc_generator.exe` without any
arguments will generate a solo with a captain rank.

```
usage: cp_red_npc_generator.exe [-h] 
                                [--rank {private,corporal,lieutenant,captain,lieutenant_colonel,lieutenant_general,general}]
                                [--role {rockerboy,solo,netrunner,tech,medtech,media,exec,lawman,fixer,nomad,civilian}]
                                [--seed SEED] 
                                [--flat | --no-flat]
                                [--log_level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]

options:
  -h, --help            show this help message and exit
  --rank {private,corporal,lieutenant,captain,lieutenant_colonel,lieutenant_general,general}
                        A measure of the development of a given NPC, where
                        private is an unskilled and unknown newcomer, and
                        general is a world-class character. Rank determines
                        how advanced an NPC's skills are and how cool his
                        equipment is.
  --role {rockerboy,solo,netrunner,tech,medtech,media,exec,lawman,fixer,nomad,civilian}
                        An occupation the NPC is known by on The Street.
                        `civilian` means that this is just a regular human.
                        The role can determine the equipment and the direction of
                        the NPC's skills. The default value is `solo`.
  --seed SEED           A number for a random engine. The same seed will
                        always give the same result when the other arguments
                        are unchanged. The default is 0, which means "use unix
                        epoch".
  --flat, --no-flat     If specified, don't use columns. Easier for editing
                        and copy-pasting, but takes much more space.
  --log_level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Logging level. Default is INFO.
```

## Examples of input and output data

<details>
  <summary>Private (the lowest rank, punching dolls for the initial characters)</summary>
  Input:

  ```
cp_red_npc_generator.exe --rank=private --role=solo
  ```

Possible output:

  ```
Solo, Private, seed=541683456
Has items total worth of 272

Conditions:
	HP: 25/25 (Seriously Wounded: 13)
	Can evade bullets: False

Stats:
	[3] INT
	[3] REF
	[3] DEX
	[2] TECH
	[3] COOL
	[3] WILL
	[2] LUCK
	[3] MOVE
	[3] BODY
	[2] EMP

Skills:
    Education                               Technique                                  Social                                  
        [3(INT)=3] Accounting                   [2(TECH)=2] AirVehicleTech                 [3(COOL)=3] Bribery                 
        [3(INT)=3] AnimalHandling               [2(TECH)=2] BasicTech                      [2(EMP)+2=4] Conversation           
        [3(INT)=3] Bureaucracy                  [2(TECH)=2] Cybertech                      [2(EMP)+2=4] HumanPerception        
        [3(INT)=3] Business                     [2(TECH)=2] Demolitions                    [3(COOL)+2=5] Interrogation         
        [3(INT)=3] Composition                  [2(TECH)=2] ElectronicsSecurityTech        [3(COOL)+2=5] Persuasion            
        [3(INT)=3] Criminology                  [2(TECH)+2=4] FirstAid                     [3(COOL)=3] PersonalGrooming        
        [3(INT)=3] Cryptography                 [2(TECH)=2] Forgery                        [3(COOL)=3] Streetwise              
        [3(INT)=3] Deduction                    [2(TECH)=2] LandVehicleTech                [3(COOL)=3] Trading                 
        [3(INT)+2=5] Education                  [2(TECH)=2] PaintDrawSculpt                [3(COOL)=3] WardrobeStyle           
        [3(INT)=3] Gamble                       [2(TECH)=2] Paramedic                  Body                                    
        [3(INT)=3] LibrarySearch                [2(TECH)=2] PhotographyFilm                [3(DEX)+2=5] Athletics              
        [3(INT)+2=5] LocalExpertYourHome        [2(TECH)=2] PickLock                       [3(DEX)=3] Contortionist            
        [3(INT)+2=5] Tactics                    [2(TECH)=2] PickPocket                     [3(DEX)=3] Dance                    
        [3(INT)=3] WildernessSurvival           [2(TECH)=2] SeaVehicleTech                 [3(WILL)=3] Endurance               
        [3(INT)+2=5] LanguageStreetslang        [2(TECH)=2] Weaponstech                    [3(WILL)+2=5] ResistTortureDrugs    
        [3(INT)=3] Science                  Awareness                                      [3(DEX)+2=5] Stealth                
    Fighting                                    [3(WILL)+2=5] Concentration            Ranged_Weapon                           
        [3(DEX)+2=5] Brawling                   [3(INT)=3] ConcealRevealObject             [3(REF)=3] Archery                  
        [3(DEX)+2=5] Evasion                    [3(INT)=3] LipReading                      [3(REF)+2=5] Autofire               
        [3(DEX)=3] MartialArts                  [3(INT)+2=5] Perception                    [3(REF)+2=5] Handgun                
        [3(DEX)+2=5] MeleeWeapon                [3(INT)=3] Tracking                        [3(REF)=3] HeavyWeapons             
        [3(REF)=3] Initiative               Control                                        [3(REF)+2=5] ShoulderArms           
    Performance                                 [3(REF)=3] DriveLandVehicle                                                    
        [3(COOL)=3] Acting                      [3(REF)=3] PilotAirVehicle                                                     
        [2(TECH)=2] PlayInstrument              [3(REF)=3] PilotSeaVehicle                                                     
                                                [3(REF)=3] Riding                                                              
    
Armor:                                          Ranged weapons:                                                                           
    Head: Leathers [20eb (everyday), SP=4/4]        Sternmeyer SMG-21 (Heavy SMG) [50eb (costly), poor, Damage=3d6, ROF=1, Mag=/40 ()]    
    Body: Leathers [20eb (everyday), SP=4/4]    Melee weapons:                                                                            
                                                    Battle axe (Medium Melee Weapon) [50eb (costly), standard, Damage=2d6, ROF=2]         
                                                    Boxing [Damage=1d6, ROF=1]                                                            

Inventory:
    Ammo                                                   Equipment / Drugs                     Junk                                   
        [1] Grenades (Armor-Piercing) [100eb (premium)]        [1] Carryall [20eb (everyday)]        [45] Eddies [1eb (cheap)]          
        [80] Bullets (Basic) [1eb (cheap)]                                                           [1] Prayer Beads [10eb (cheap)]    
                                                                                                     [1] Broken Eye Implant             
                                                                                                     [1] Damaged Clothes                
                                                                                                     [1] Storage Locker Key             
                                                                                                     [1] Fluorescent Lipstick           
                                                                                                     [1] Stapler                        
  ```

</details>

<details>
  <summary>Captain (equivalent of the players' starting characters)</summary>
  Input:

  ```
cp_red_npc_generator.exe --rank=captain --role=solo
  ```

Possible output:

  ```
Solo, Captain, seed=521984000
Has items total worth of 1872

Conditions:
	HP: 45/45 (Seriously Wounded: 23)
	Can evade bullets: True (REF >= 8)

Stats:
	[7] INT
	[8] REF
	[7] DEX
	[5] TECH
	[6] COOL
	[6] WILL
	[5] LUCK
	[6] MOVE
	[8] BODY
	[3] EMP

Skills:
    Education                               Technique                                  Social                                   
        [7(INT)=7] Accounting                   [5(TECH)=5] AirVehicleTech                 [6(COOL)=6] Bribery                  
        [7(INT)=7] AnimalHandling               [5(TECH)=5] BasicTech                      [3(EMP)+2=5] Conversation            
        [7(INT)=7] Bureaucracy                  [5(TECH)=5] Cybertech                      [3(EMP)+2=5] HumanPerception         
        [7(INT)=7] Business                     [5(TECH)=5] Demolitions                    [6(COOL)+6=12] Interrogation         
        [7(INT)=7] Composition                  [5(TECH)=5] ElectronicsSecurityTech        [6(COOL)+2=8] Persuasion             
        [7(INT)=7] Criminology                  [5(TECH)+6=11] FirstAid                    [6(COOL)=6] PersonalGrooming         
        [7(INT)=7] Cryptography                 [5(TECH)=5] Forgery                        [6(COOL)=6] Streetwise               
        [7(INT)=7] Deduction                    [5(TECH)=5] LandVehicleTech                [6(COOL)=6] Trading                  
        [7(INT)+2=9] Education                  [5(TECH)=5] PaintDrawSculpt                [6(COOL)=6] WardrobeStyle            
        [7(INT)=7] Gamble                       [5(TECH)=5] Paramedic                  Body                                     
        [7(INT)=7] LibrarySearch                [5(TECH)=5] PhotographyFilm                [7(DEX)+2=9] Athletics               
        [7(INT)+2=9] LocalExpertYourHome        [5(TECH)=5] PickLock                       [7(DEX)=7] Contortionist             
        [7(INT)+6=13] Tactics                   [5(TECH)=5] PickPocket                     [7(DEX)=7] Dance                     
        [7(INT)=7] WildernessSurvival           [5(TECH)=5] SeaVehicleTech                 [6(WILL)=6] Endurance                
        [7(INT)+2=9] LanguageStreetslang        [5(TECH)=5] Weaponstech                    [6(WILL)+6=12] ResistTortureDrugs    
        [7(INT)=7] Science                  Awareness                                      [7(DEX)+2=9] Stealth                 
    Fighting                                    [6(WILL)+2=8] Concentration            Ranged_Weapon                            
        [7(DEX)+2=9] Brawling                   [7(INT)=7] ConcealRevealObject             [8(REF)=8] Archery                   
        [7(DEX)+6=13] Evasion                   [7(INT)=7] LipReading                      [8(REF)+6=14] Autofire               
        [7(DEX)=7] MartialArts                  [7(INT)+6=13] Perception                   [8(REF)+6=14] Handgun                
        [7(DEX)+6=13] MeleeWeapon               [7(INT)=7] Tracking                        [8(REF)=8] HeavyWeapons              
        [8(REF)=8] Initiative               Control                                        [8(REF)+6=14] ShoulderArms           
    Performance                                 [8(REF)=8] DriveLandVehicle                                                     
        [6(COOL)=6] Acting                      [8(REF)=8] PilotAirVehicle                                                      
        [5(TECH)=5] PlayInstrument              [8(REF)=8] PilotSeaVehicle                                                      
                                                [8(REF)=8] Riding                                                               
    
Cyberware:
    Borgware                                           
        Cyclops International Bug Eye [500eb] [1/5]    
            Targeting Scope [500eb]                    
    
Armor:                                                   Ranged weapons:                                                                                 
    Head: Light Armorjack [100eb (premium), SP=11/11]        Sternmeyer SMG-21 (Heavy SMG) [100eb (premium), standard, Damage=3d6, ROF=1, Mag=/40 ()]    
    Body: Light Armorjack [100eb (premium), SP=11/11]    Melee weapons:                                                                                  
                                                             War hammer (Heavy Melee Weapon) [100eb (premium), standard, Damage=3d6, ROF=2]              
                                                             Boxing [Damage=3d6, ROF=1]                                                                  

Inventory:
    Ammo                                                   Equipment / Drugs                               Junk                                                                        
        [1] Grenades (Armor-Piercing) [100eb (premium)]        [1] Radio Communicator [100eb (premium)]        [503] Eddies [1eb (cheap)]                                              
        [80] Bullets (Basic) [1eb (cheap)]                     [1] Airhypo [50eb (costly)]                     [1] Expensive Necklace [100eb (premium)]                                
                                                               [1] Black Lace [50eb (costly)]                  [1] Autographed Photograph of Night City Celebrity [20eb (everyday)]    
                                                               [2] Synthcoke [20eb (everyday)]                 [1] Glow Stick [10eb (cheap)]                                           
                                                               [1] Carryall [20eb (everyday)]                                                                                          
  ```

</details>

<details>
  <summary>General (Adam Smasher)</summary>
  Input:

  ```
cp_red_npc_generator.exe --rank=general --role=solo
  ```

Possible output:

  ```
Solo, General, seed=924241408
Has items total worth of 40532

Conditions:
	HP: 50/50 (Seriously Wounded: No, Pain Editor)
	TraumaTeam status: EXECUTIVE
	Can evade bullets: False

Stats:
	[7] INT
	[8-4(Head: Metalgear)=4] REF
	[8-4(Head: Metalgear)=4] DEX
	[5] TECH
	[8] COOL
	[8] WILL
	[8] LUCK
	[7-4(Head: Metalgear)=3] MOVE
	[8+2(Grafted Muscle and Bone Lace)+4(Implanted Linear Frame ß (Beta))=14] BODY
	[0] EMP

Skills:
    Education                                   Technique                                  Social                                   
        [7(INT)=7] Accounting                       [5(TECH)=5] AirVehicleTech                 [8(COOL)=8] Bribery                  
        [7(INT)=7] AnimalHandling                   [5(TECH)=5] BasicTech                      [0(EMP)+3=3] Conversation            
        [7(INT)=7] Bureaucracy                      [5(TECH)=5] Cybertech                      [0(EMP)+3=3] HumanPerception         
        [7(INT)=7] Business                         [5(TECH)=5] Demolitions                    [8(COOL)+8=16] Interrogation         
        [7(INT)=7] Composition                      [5(TECH)=5] ElectronicsSecurityTech        [8(COOL)+3=11] Persuasion            
        [7(INT)=7] Criminology                      [5(TECH)+8=13] FirstAid                    [8(COOL)=8] PersonalGrooming         
        [7(INT)=7] Cryptography                     [5(TECH)=5] Forgery                        [8(COOL)=8] Streetwise               
        [7(INT)=7] Deduction                        [5(TECH)=5] LandVehicleTech                [8(COOL)=8] Trading                  
        [7(INT)+3=10] Education                     [5(TECH)=5] PaintDrawSculpt                [8(COOL)=8] WardrobeStyle            
        [7(INT)=7] Gamble                           [5(TECH)=5] Paramedic                  Body                                     
        [7(INT)=7] LibrarySearch                    [5(TECH)=5] PhotographyFilm                [4(DEX)+3=7] Athletics               
        [7(INT)+3=10] LocalExpertYourHome           [5(TECH)=5] PickLock                       [4(DEX)=4] Contortionist             
        [7(INT)+8=15] Tactics                       [5(TECH)=5] PickPocket                     [4(DEX)=4] Dance                     
        [7(INT)=7] WildernessSurvival               [5(TECH)=5] SeaVehicleTech                 [8(WILL)=8] Endurance                
        [7(INT)+3=10] LanguageStreetslang           [5(TECH)=5] Weaponstech                    [8(WILL)+8=16] ResistTortureDrugs    
        [7(INT)=7] Science                      Awareness                                      [4(DEX)+3=7] Stealth                 
    Fighting                                        [8(WILL)+3=11] Concentration           Ranged_Weapon                            
        [4(DEX)+3=7] Brawling                       [7(INT)=7] ConcealRevealObject             [4(REF)=4] Archery                   
        [4(DEX)+8=12] Evasion                       [7(INT)=7] LipReading                      [4(REF)+8=12] Autofire               
        [4(DEX)=4] MartialArts                      [7(INT)+8=15] Perception                   [4(REF)+8=12] Handgun                
        [4(DEX)+8=12] MeleeWeapon                   [7(INT)=7] Tracking                        [4(REF)=4] HeavyWeapons              
        [4(REF)+3(Sandevistan)=7] Initiative    Control                                        [4(REF)+8=12] ShoulderArms           
    Performance                                     [4(REF)=4] DriveLandVehicle                                                     
        [8(COOL)=8] Acting                          [4(REF)=4] PilotAirVehicle                                                      
        [5(TECH)=5] PlayInstrument                  [4(REF)=4] PilotSeaVehicle                                                      
                                                    [4(REF)=4] Riding                                                               
    
Cyberware:
    Borgware                                           Shoulders [2/2]                                                      Internal Cyberware [5/7]                                   
        Cyclops International Bug Eye [500eb] [3/5]        Cyberarm [500eb] [4/4]                                               Internal Body Cyberware Hardened Shielding [1000eb]    
            Low Light / Infrared / UV [500eb]                  Popup Ranged Weapon (SMG) [500eb]                                Independent Air Supply [1000eb]                        
            Targeting Scope [500eb]                            Flashbulb [500eb]                                                Grafted Muscle and Bone Lace [1000eb]                  
        Implanted Linear Frame ß (Beta) [5000eb]           Cyberarm [500eb] [4/4]                                               Grafted Muscle and Bone Lace [1000eb]                  
        Artificial Shoulder Mount [1000eb] [2/2]               Popup Grenade Launcher [500eb]                                   Appetite Controller [500eb]                            
            Cyberarm [500eb] [3/4]                             Dynalar Modular Finger Enthusiast Cyberhand [500eb] [1/8]    Neuralware [1/1]                                           
                Popup Net Launcher [500eb]                         Airhypo Cyberfinger [100eb]                                  Neural Link [500eb] [2/5]                              
            Cyberarm [500eb] [4/4]                     Auditory System [1/1]                                                        Sandevistan [500eb]                                
                ChainRipp [500eb]                          Cyberaudio Suite [500eb] [1/3]                                           Chipware Socket [500eb] [1/1]                      
        Artificial Shoulder Mount [1000eb] [1/2]               Sensor Array [1000eb] [0/5]                                              Pain Editor [1000eb]                           
            Cyberarm [500eb] [3/4]                             Radio Communicator [100eb]                                   Eye Sockets [1/2]                                          
                Popup Shield [500eb]                   Fashionware [2/7]                                                        Cybereye [100eb] [2/3]                                 
    External Cyberware [1/7]                               Biomonitor [100eb]                                                       Low Light / Infrared / UV [500eb]                  
        Kiroshi OptiShield [500eb]                         Kill Display [100eb]                                                                                                        
    
Armor:                                             Ranged weapons:                                                                                               
    Head: Metalgear [5000eb (luxury), SP=18/18]        Popup Grenade Launcher [500eb (expensive), Damage=6d6, ROF=1, Mag=/2 ()]                                  
    Body: Metalgear [5000eb (luxury), SP=18/18]        GunMart "Snipe-Star" (Sniper Rifle) [1000eb (very_expensive), excellent, Damage=5d6, ROF=1, Mag=/4 ()]    
    Popup Shield [500eb (expensive), SP=10/10]         Popup Ranged Weapon (SMG) [500eb (expensive), Damage=2d6, ROF=1, Mag=/30 ()]                              
                                                       Popup Net Launcher [500eb (expensive), Damage=0d0, ROF=1, Mag=/1 ()]                                      
                                                   Melee weapons:                                                                                                
                                                       Spiked Bat (Heavy Melee Weapon) [500eb (expensive), excellent, Damage=3d6, ROF=2]                         
                                                       ChainRipp [500eb (expensive), excellent, Damage=4d6, ROF=1]                                               
                                                       Boxing [Damage=4d6, ROF=1]                                                                                

Inventory:
    Ammo                                                Equipment / Drugs                                                        Junk                                                          
        [30] Bullets (Armor-Piercing) [10eb (cheap)]        [1] Auto Level Dampening Ear Protectors [1000eb (very_expensive)]        [2840] Eddies [1eb (cheap)]                               
        [2] Grenades (Smoke) [50eb (costly)]                [1] Radar Detector [500eb (expensive)]                                   [1] Gold Ring with Engraved Initials [100eb (premium)]    
        [2] Net (Net) [50eb (costly)]                       [2] Berserker [100eb (premium)]                                          [1] Good Beer [20eb (everyday)]                           
        [30] Bullets (Basic) [1eb (cheap)]                  [2] Timewarp [100eb (premium)]                                           [1] Kibble Pack [10eb (cheap)]                            
                                                            [2] Black Lace [50eb (costly)]                                           [1] A pair of six-sided dice                              
                                                            [2] Synthcoke [20eb (everyday)]                                                                                                    
                                                            [1] Flashlight [20eb (everyday)]                                                                                                   
    
  ```

</details>

## Limitations (or todos? who knows)

* No skill chips
* Skills - only upgrades to street rat
* (Almost) only items from the basic rulebook
* No weapon modifications
* No exotic weapons
