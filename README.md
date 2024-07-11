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
Solo, Private, seed=911573248
Has items total worth of 182

Health (you can add conditions here):
	HP: 25/25 (Seriously Wounded: 13)

Stats:
	[3] INT
	[3] REF
	[3] DEX
	[2] TECH
	[3] COOL
	[3] WILL
	[3] LUCK
	[3] MOVE
	[3] BODY
	[2] EMP

Skills:
    Education                               Technique                                  Social                                  
        [3(INT)=3] Accounting                   [2(TECH)=2] AirVehicleTech                 [3(COOL)=3] Bribery                 
        [3(INT)=3] AnimalHandling               [2(TECH)=2] BasicTech                      [2(EMP)+2=4] Conversation           
        [3(INT)=3] Bureaucracy                  [2(TECH)=2] Cybertech                      [2(EMP)+2=4] HumanPerception        
        [3(INT)=3] Business                     [2(TECH)=2] Demolitions                    [3(COOL)+3=6] Interrogation         
        [3(INT)=3] Composition                  [2(TECH)=2] ElectronicsSecurityTech        [3(COOL)+2=5] Persuasion            
        [3(INT)=3] Criminology                  [2(TECH)+3=5] FirstAid                     [3(COOL)=3] PersonalGrooming        
        [3(INT)=3] Cryptography                 [2(TECH)=2] Forgery                        [3(COOL)=3] Streetwise              
        [3(INT)=3] Deduction                    [2(TECH)=2] LandVehicleTech                [3(COOL)=3] Trading                 
        [3(INT)+2=5] Education                  [2(TECH)=2] PaintDrawSculpt                [3(COOL)=3] WardrobeStyle           
        [3(INT)=3] Gamble                       [2(TECH)=2] Paramedic                  Body                                    
        [3(INT)=3] LibrarySearch                [2(TECH)=2] PhotographyFilm                [3(DEX)+2=5] Athletics              
        [3(INT)+2=5] LocalExpertYourHome        [2(TECH)=2] PickLock                       [3(DEX)=3] Contortionist            
        [3(INT)+3=6] Tactics                    [2(TECH)=2] PickPocket                     [3(DEX)=3] Dance                    
        [3(INT)=3] WildernessSurvival           [2(TECH)=2] SeaVehicleTech                 [3(WILL)=3] Endurance               
        [3(INT)+2=5] LanguageStreetslang        [2(TECH)=2] Weaponstech                    [3(WILL)+3=6] ResistTortureDrugs    
        [3(INT)=3] Science                  Awareness                                      [3(DEX)+2=5] Stealth                
    Fighting                                    [3(WILL)+2=5] Concentration            Ranged_Weapon                           
        [3(DEX)+2=5] Brawling                   [3(INT)=3] ConcealRevealObject             [3(REF)=3] Archery                  
        [3(DEX)+3=6] Evasion                    [3(INT)=3] LipReading                      [3(REF)+3=6] Autofire               
        [3(DEX)=3] MartialArts                  [3(INT)+3=6] Perception                    [3(REF)+3=6] Handgun                
        [3(DEX)+3=6] MeleeWeapon                [3(INT)=3] Tracking                        [3(REF)=3] HeavyWeapons             
        [3(REF)=3] Initiative               Control                                        [3(REF)+3=6] ShoulderArms           
    Performance                                 [3(REF)=3] DriveLandVehicle                                                    
        [3(COOL)=3] Acting                      [3(REF)=3] PilotAirVehicle                                                     
        [2(TECH)=2] PlayInstrument              [3(REF)=3] PilotSeaVehicle                                                     
                                                [3(REF)=3] Riding                                                              
    
Armor:                                          Ranged weapons:                                                                           
    Head: Leathers [20eb (everyday), SP=4/4]        Sternmeyer SMG-21 (Heavy SMG) [50eb (costly), poor, Damage=3d6, ROF=1, Mag=/40 ()]    
    Body: Leathers [20eb (everyday), SP=4/4]    Melee weapons:                                                                            
                                                    Spiked Bat (Heavy Melee Weapon) [50eb (costly), poor, Damage=3d6, ROF=2]              
                                                    Boxing [Damage=1d6, ROF=1]                                                            

Inventory:
    Ammo                                      Equipment / Drugs                             Junk                                                
        [35] Bullets (Basic) [1eb (cheap)]        [1] Personal CarePak [20eb (everyday)]        [52] Eddies [1eb (cheap)]                       
                                                                                                [1] Pocket Mirror [10eb (cheap)]                
                                                                                                [1] Incense [10eb (cheap)]                      
                                                                                                [1] Plastic Earring                             
                                                                                                [1] Class Schedule for Night City University    
                                                                                                [1] Rock        
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
Solo, Captain, seed=953609728
Has items total worth of 1682

Health (you can add conditions here):
	HP: 45/45 (Seriously Wounded: 23)

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
        [7(INT)=7] Business                     [5(TECH)=5] Demolitions                    [6(COOL)+7=13] Interrogation         
        [7(INT)=7] Composition                  [5(TECH)=5] ElectronicsSecurityTech        [6(COOL)+2=8] Persuasion             
        [7(INT)=7] Criminology                  [5(TECH)+7=12] FirstAid                    [6(COOL)=6] PersonalGrooming         
        [7(INT)=7] Cryptography                 [5(TECH)=5] Forgery                        [6(COOL)=6] Streetwise               
        [7(INT)=7] Deduction                    [5(TECH)=5] LandVehicleTech                [6(COOL)=6] Trading                  
        [7(INT)+2=9] Education                  [5(TECH)=5] PaintDrawSculpt                [6(COOL)=6] WardrobeStyle            
        [7(INT)=7] Gamble                       [5(TECH)=5] Paramedic                  Body                                     
        [7(INT)=7] LibrarySearch                [5(TECH)=5] PhotographyFilm                [7(DEX)+2=9] Athletics               
        [7(INT)+2=9] LocalExpertYourHome        [5(TECH)=5] PickLock                       [7(DEX)=7] Contortionist             
        [7(INT)+7=14] Tactics                   [5(TECH)=5] PickPocket                     [7(DEX)=7] Dance                     
        [7(INT)=7] WildernessSurvival           [5(TECH)=5] SeaVehicleTech                 [6(WILL)=6] Endurance                
        [7(INT)+2=9] LanguageStreetslang        [5(TECH)=5] Weaponstech                    [6(WILL)+7=13] ResistTortureDrugs    
        [7(INT)=7] Science                  Awareness                                      [7(DEX)+2=9] Stealth                 
    Fighting                                    [6(WILL)+2=8] Concentration            Ranged_Weapon                            
        [7(DEX)+2=9] Brawling                   [7(INT)=7] ConcealRevealObject             [8(REF)=8] Archery                   
        [7(DEX)+7=14] Evasion                   [7(INT)=7] LipReading                      [8(REF)+7=15] Autofire               
        [7(DEX)=7] MartialArts                  [7(INT)+7=14] Perception                   [8(REF)+7=15] Handgun                
        [7(DEX)+7=14] MeleeWeapon               [7(INT)=7] Tracking                        [8(REF)=8] HeavyWeapons              
        [8(REF)=8] Initiative               Control                                        [8(REF)+7=15] ShoulderArms           
    Performance                                 [8(REF)=8] DriveLandVehicle                                                     
        [6(COOL)=6] Acting                      [8(REF)=8] PilotAirVehicle                                                      
        [5(TECH)=5] PlayInstrument              [8(REF)=8] PilotSeaVehicle                                                      
                                                [8(REF)=8] Riding                                                               
    
Cyberware:
    Auditory System [1/1]                 Fashionware [1/7]         Shoulders [1/2]           
        Cyberaudio Suite [500eb] [2/3]        Biomonitor [100eb]        Big Knucks [100eb]    
            Radio Communicator [100eb]                                                        
            Level Damper [100eb]                                                              
    
Armor:                                                   Ranged weapons:                                                                                
    Head: Light Armorjack [100eb (premium), SP=11/11]        Militech "Viper" (Heavy SMG) [100eb (premium), standard, Damage=3d6, ROF=1, Mag=/40 ()]    
    Body: Light Armorjack [100eb (premium), SP=11/11]    Melee weapons:                                                                                 
                                                             Big Knucks [100eb (premium), Damage=2d6, ROF=2]                                            
                                                             Boxing [Damage=3d6, ROF=1]                                                                 

Inventory:
    Ammo                                        Equipment / Drugs                                     Junk                                                    
        [80] Bullets (Basic) [1eb (cheap)]          [1] Berserker [100eb (premium)]                       [531] Eddies [1eb (cheap)]                          
        [1] Grenades (Smoke) [50eb (costly)]        [1] Airhypo [50eb (costly)]                           [1] Flask of Expensive Alcohol [100eb (premium)]    
                                                    [1] Anti-Smog Breathing Mask [20eb (everyday)]                                                            
                                                    [1] Carryall [20eb (everyday)]                                                                            
                                                    [1] Flashlight [20eb (everyday)]                                                                          
                                                    [1] Personal CarePak [20eb (everyday)]                                                                        
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
Solo, General, seed=54158848
Has items total worth of 30004

Health (you can add conditions here):
	HP: 50/50 (Seriously Wounded: No, Pain Editor)

Stats:
	[8] INT
	[8-4(Body: Metalgear)=4] REF
	[8-4(Body: Metalgear)=4] DEX
	[6] TECH
	[8] COOL
	[8] WILL
	[6] LUCK
	[8-4(Body: Metalgear)=4] MOVE
	[8+2(Grafted Muscle and Bone Lace)+4(Implanted Linear Frame ß (Beta))=14] BODY
	[0] EMP

Skills:
    Education                                   Technique                                  Social                                   
        [8(INT)=8] Accounting                       [6(TECH)=6] AirVehicleTech                 [8(COOL)=8] Bribery                  
        [8(INT)=8] AnimalHandling                   [6(TECH)=6] BasicTech                      [0(EMP)+3=3] Conversation            
        [8(INT)=8] Bureaucracy                      [6(TECH)=6] Cybertech                      [0(EMP)+3=3] HumanPerception         
        [8(INT)=8] Business                         [6(TECH)=6] Demolitions                    [8(COOL)+8=16] Interrogation         
        [8(INT)=8] Composition                      [6(TECH)=6] ElectronicsSecurityTech        [8(COOL)+3=11] Persuasion            
        [8(INT)=8] Criminology                      [6(TECH)+8=14] FirstAid                    [8(COOL)=8] PersonalGrooming         
        [8(INT)=8] Cryptography                     [6(TECH)=6] Forgery                        [8(COOL)=8] Streetwise               
        [8(INT)=8] Deduction                        [6(TECH)=6] LandVehicleTech                [8(COOL)=8] Trading                  
        [8(INT)+3=11] Education                     [6(TECH)=6] PaintDrawSculpt                [8(COOL)=8] WardrobeStyle            
        [8(INT)=8] Gamble                           [6(TECH)=6] Paramedic                  Body                                     
        [8(INT)=8] LibrarySearch                    [6(TECH)=6] PhotographyFilm                [4(DEX)+3=7] Athletics               
        [8(INT)+3=11] LocalExpertYourHome           [6(TECH)=6] PickLock                       [4(DEX)=4] Contortionist             
        [8(INT)+8=16] Tactics                       [6(TECH)=6] PickPocket                     [4(DEX)=4] Dance                     
        [8(INT)=8] WildernessSurvival               [6(TECH)=6] SeaVehicleTech                 [8(WILL)=8] Endurance                
        [8(INT)+3=11] LanguageStreetslang           [6(TECH)=6] Weaponstech                    [8(WILL)+8=16] ResistTortureDrugs    
        [8(INT)=8] Science                      Awareness                                      [4(DEX)+3=7] Stealth                 
    Fighting                                        [8(WILL)+3=11] Concentration           Ranged_Weapon                            
        [4(DEX)+3=7] Brawling                       [8(INT)=8] ConcealRevealObject             [4(REF)=4] Archery                   
        [4(DEX)+8=12] Evasion                       [8(INT)=8] LipReading                      [4(REF)+8=12] Autofire               
        [4(DEX)=4] MartialArts                      [8(INT)+8=16] Perception                   [4(REF)+8=12] Handgun                
        [4(DEX)+8=12] MeleeWeapon                   [8(INT)=8] Tracking                        [4(REF)=4] HeavyWeapons              
        [4(REF)+3(Sandevistan)=7] Initiative    Control                                        [4(REF)+8=12] ShoulderArms           
    Performance                                     [4(REF)=4] DriveLandVehicle                                                     
        [8(COOL)=8] Acting                          [4(REF)=4] PilotAirVehicle                                                      
        [6(TECH)=6] PlayInstrument                  [4(REF)=4] PilotSeaVehicle                                                      
                                                    [4(REF)=4] Riding                                                               
    
Cyberware:
    Eye Sockets [2/2]                            Neuralware [1/1]                                Shoulders [2/2]                              
        Cybereye [100eb] [3/3]                       Neural Link [500eb] [2/5]                       Cyberarm [500eb] [4/4]                   
            Anti-Dazzle [100eb]                          Sandevistan [500eb]                             Popup Grenade Launcher [500eb]       
            Low Light / Infrared / UV [500eb]            Chipware Socket [500eb] [1/1]                   Popup Ranged Weapon (SMG) [500eb]    
        Cybereye [100eb] [3/3]                               Pain Editor [1000eb]                    Big Knucks [100eb]                       
            Anti-Dazzle [100eb]                  Borgware                                        Auditory System [1/1]                        
            Low Light / Infrared / UV [500eb]        Implanted Linear Frame ß (Beta) [5000eb]        Cyberaudio Suite [500eb] [2/3]           
    Internal Cyberware [2/7]                         Artificial Shoulder Mount [1000eb] [1/2]            Level Damper [100eb]                 
        Grafted Muscle and Bone Lace [1000eb]            Cyberarm [500eb] [3/4]                          Radar Detector [500eb]               
        Grafted Muscle and Bone Lace [1000eb]                Popup Shield [500eb]                Fashionware [1/7]                            
                                                                                                     Biomonitor [100eb]                       
    
Armor:                                             Ranged weapons:                                                                                             
    Head: Metalgear [5000eb (luxury), SP=18/18]        Popup Grenade Launcher [500eb (expensive), Damage=6d6, ROF=1, Mag=/2 ()]                                
    Body: Metalgear [5000eb (luxury), SP=18/18]        Arasaka "Rapid Assault" (Shotgun) [1000eb (very_expensive), excellent, Damage=5d6, ROF=1, Mag=/4 ()]    
    Popup Shield [500eb (expensive), SP=10/10]         Popup Ranged Weapon (SMG) [500eb (expensive), Damage=2d6, ROF=1, Mag=/30 ()]                            
                                                   Melee weapons:                                                                                              
                                                       Spiked Bat (Heavy Melee Weapon) [500eb (expensive), excellent, Damage=3d6, ROF=2]                       
                                                       Boxing [Damage=4d6, ROF=1]                                                                              
                                                       Big Knucks [100eb (premium), Damage=2d6, ROF=2]                                                         

Inventory:
    Ammo                                                   Equipment / Drugs                                     Junk                                        
        [2] Grenades (Armor-Piercing) [100eb (premium)]        [2] Berserker [100eb (premium)]                       [2573] Eddies [1eb (cheap)]             
        [2] Grenades (Teargas) [50eb (costly)]                 [2] Timewarp [100eb (premium)]                        [1] Golden Chain [500eb (expensive)]    
        [60] Bullets (Basic) [1eb (cheap)]                     [1] Radio Communicator [100eb (premium)]              [1] Hand Fan [10eb (cheap)]             
        [4] Shotgun Shells (Incendiary) [10eb (cheap)]         [2] Black Lace [50eb (costly)]                        [1] Incense [10eb (cheap)]              
        [4] Slugs (Expansive) [10eb (cheap)]                   [1] Airhypo [50eb (costly)]                                                                   
        [4] Slugs (Armor-Piercing) [10eb (cheap)]              [1] Carryall [20eb (everyday)]                                                                
        [32] Slugs (Basic) [1eb (cheap)]                       [1] Anti-Smog Breathing Mask [20eb (everyday)]                                                
        [20] Shotgun Shells (Basic) [1eb (cheap)]              [1] Flashlight [20eb (everyday)]                                                              
                                                               [1] Personal CarePak [20eb (everyday)]                                                        
                                                               [1] Synthcoke [20eb (everyday)]                                                               
  ```

</details>

## Limitations (or todos? who knows)

* No skill chips
* Skills - only upgrades to street rat
* (Almost) only items from the basic rulebook
* No weapon modifications
* No exotic weapons
