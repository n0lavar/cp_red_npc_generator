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

```
usage: cp_red_npc_generator.exe [-h] --rank
                                {private,corporal,lieutenant,captain,lieutenant_colonel,lieutenant_general,general}
                                [--role {rockerboy,solo,netrunner,tech,medtech,media,exec,lawman,fixer,nomad,civilian,booster}]
                                [--seed SEED] [--flat | --no-flat]
                                [--log_level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]

options:
  -h, --help            show this help message and exit
  --rank {private,corporal,lieutenant,captain,lieutenant_colonel,lieutenant_general,general}
                        A measure of the development of a given NPC, where
                        private is an unskilled and unknown newcomer, and
                        general is a world-class character. Rank determines
                        how advanced an NPC's skills are and how cool his
                        equipment is.
  --role {rockerboy,solo,netrunner,tech,medtech,media,exec,lawman,fixer,nomad,civilian,booster}
                        An occupation the NPC is known by on The Street.
                        `civilian` means that this is just a regular human,
                        `booster` means that this is a street mook with some
                        fighting skills, but without any specialization. The
                        role can determine the equipment and the direction of
                        the NPC's skills. The default value is `booster`.
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

Output:

  ```
Solo, Private, seed=1718139711
Has items total worth of 252

Health (you can add conditions here):
	HP: 25/25 (Seriously Wounded: 13)

Stats: (stat+modifiers=total)
	[3] INT | [3] REF | [4] DEX | [3] TECH | [3] COOL | [3] WILL | [3] LUCK | [3] MOVE | [3] BODY | [2] EMP

Skills (stat+skill+modifiers=total):
    Education                            Technique                                Social                            Body                                 
        [3+0+0=3] Accounting                 [3+0+0=3] AirVehicleTech                 [3+0+0=3] Bribery                 [4+2+0=6] Athletics              
        [3+0+0=3] AnimalHandling             [3+0+0=3] BasicTech                      [2+2+0=4] Conversation            [4+0+0=4] Contortionist          
        [3+0+0=3] Bureaucracy                [3+0+0=3] Cybertech                      [2+2+0=4] HumanPerception         [4+0+0=4] Dance                  
        [3+0+0=3] Business                   [3+0+0=3] Demolitions                    [3+3+0=6] Interrogation           [3+0+0=3] Endurance              
        [3+0+0=3] Composition                [3+0+0=3] ElectronicsSecurityTech        [3+2+0=5] Persuasion              [3+3+2=8] ResistTortureDrugs     
        [3+0+0=3] Criminology                [3+3+0=6] FirstAid                       [3+0+0=3] PersonalGrooming        [4+2+0=6] Stealth                
        [3+0+0=3] Cryptography               [3+0+0=3] Forgery                        [3+0+0=3] Streetwise          Awareness                            
        [3+0+0=3] Deduction                  [3+0+0=3] LandVehicleTech                [3+0+0=3] Trading                 [3+2+0=5] Concentration          
        [3+2+0=5] Education                  [3+0+0=3] PaintDrawSculpt                [3+0+0=3] WardrobeStyle           [3+0+0=3] ConcealRevealObject    
        [3+0+0=3] Gamble                     [3+0+0=3] Paramedic                  Fighting                              [3+0+0=3] LipReading             
        [3+0+0=3] LibrarySearch              [3+0+0=3] PhotographyFilm                [4+2+0=6] Brawling                [3+3+0=6] Perception             
        [3+2+0=5] LocalExpertYourHome        [3+0+0=3] PickLock                       [4+3+0=7] Evasion                 [3+0+0=3] Tracking               
        [3+3+0=6] Tactics                    [3+0+0=3] PickPocket                     [4+0+0=4] MartialArts         Ranged_Weapon                        
        [3+0+0=3] WildernessSurvival         [3+0+0=3] SeaVehicleTech                 [4+3+0=7] MeleeWeapon             [3+0+0=3] Archery                
        [3+2+0=5] LanguageStreetslang        [3+0+0=3] Weaponstech                    [3+0+0=3] Initiative              [3+3+0=6] Autofire               
        [3+0+0=3] Science                Control                                  Performance                           [3+3+0=6] Handgun                
                                             [3+0+0=3] DriveLandVehicle               [3+0+0=3] Acting                  [3+0+0=3] HeavyWeapons           
                                             [3+0+0=3] PilotAirVehicle                [3+0+0=3] PlayInstrument          [3+3+0=6] ShoulderArms           
                                             [3+0+0=3] PilotSeaVehicle                                                                                   
                                             [3+0+0=3] Riding                                                                                            
    
Cyberware:
    Internal Cyberware [1/7]     
        Toxin Binders [100eb]    
    
Armor:                                          Ranged weapons:                                                                                
    Body: Leathers [20eb (everyday), SP=4/4]        GunMart "Home Defender" (Shotgun) [100eb (premium), poor, Damage=5d6, ROF=1, Mag=/4 ()]    
                                                Melee weapons:                                                                                 
                                                    Boxing [Damage=1d6, ROF=1]                                                                 

Inventory:
    Ammo                                    Equipment / Drugs                             Junk                                                  
        [24] Slugs (Basic) [1eb (cheap)]        [1] Personal CarePak [20eb (everyday)]        [50] Eddies [1eb (cheap)]                         
                                                                                              [1] Memory Chip (Personal Data) [10eb (cheap)]    
                                                                                              [1] Drink Umbrella                                
                                                                                              [1] Rock                                          
                                                                                              [1] Poker Chip                                    
                                                                                              [1] Pack of matches                               
                                                                                              [1] Class Schedule for Night City University      
                                                                                              [1] Stress Ball                                   
  ```

</details>

<details>
  <summary>Captain (equivalent of the players' starting characters)</summary>
  Input:

  ```
cp_red_npc_generator.exe --rank=captain --role=solo
  ```

Output:

  ```
Solo, Captain, seed=1718139817
Has items total worth of 1902

Health (you can add conditions here):
	HP: 45/45 (Seriously Wounded: 23)

Stats: (stat+modifiers=total)
	[6] INT | [7] REF | [7] DEX | [3] TECH | [8] COOL | [6] WILL | [5] LUCK | [5] MOVE | [6] BODY | [4] EMP

Skills (stat+skill+modifiers=total):
    Education                            Technique                                Social                            Body                                 
        [6+0+0=6] Accounting                 [3+0+0=3] AirVehicleTech                 [8+0+0=8] Bribery                 [7+2+0=9] Athletics              
        [6+0+0=6] AnimalHandling             [3+0+0=3] BasicTech                      [4+2+0=6] Conversation            [7+0+0=7] Contortionist          
        [6+0+0=6] Bureaucracy                [3+0+0=3] Cybertech                      [4+2+0=6] HumanPerception         [7+0+0=7] Dance                  
        [6+0+0=6] Business                   [3+0+0=3] Demolitions                    [8+6+0=14] Interrogation          [6+0+0=6] Endurance              
        [6+0+0=6] Composition                [3+0+0=3] ElectronicsSecurityTech        [8+2+0=10] Persuasion             [6+6+2=14] ResistTortureDrugs    
        [6+0+0=6] Criminology                [3+6+0=9] FirstAid                       [8+0+0=8] PersonalGrooming        [7+2+0=9] Stealth                
        [6+0+0=6] Cryptography               [3+0+0=3] Forgery                        [8+0+0=8] Streetwise          Awareness                            
        [6+0+0=6] Deduction                  [3+0+0=3] LandVehicleTech                [8+0+0=8] Trading                 [6+2+0=8] Concentration          
        [6+2+0=8] Education                  [3+0+0=3] PaintDrawSculpt                [8+0+0=8] WardrobeStyle           [6+0+0=6] ConcealRevealObject    
        [6+0+0=6] Gamble                     [3+0+0=3] Paramedic                  Fighting                              [6+0+0=6] LipReading             
        [6+0+0=6] LibrarySearch              [3+0+0=3] PhotographyFilm                [7+2+0=9] Brawling                [6+6+0=12] Perception            
        [6+2+0=8] LocalExpertYourHome        [3+0+0=3] PickLock                       [7+6+0=13] Evasion                [6+0+0=6] Tracking               
        [6+6+0=12] Tactics                   [3+0+0=3] PickPocket                     [7+0+0=7] MartialArts         Ranged_Weapon                        
        [6+0+0=6] WildernessSurvival         [3+0+0=3] SeaVehicleTech                 [7+6+0=13] MeleeWeapon            [7+0+0=7] Archery                
        [6+2+0=8] LanguageStreetslang        [3+0+0=3] Weaponstech                    [7+0+0=7] Initiative              [7+6+0=13] Autofire              
        [6+0+0=6] Science                Control                                  Performance                           [7+6+0=13] Handgun               
                                             [7+0+0=7] DriveLandVehicle               [8+0+0=8] Acting                  [7+0+0=7] HeavyWeapons           
                                             [7+0+0=7] PilotAirVehicle                [3+0+0=3] PlayInstrument          [7+6+0=13] ShoulderArms          
                                             [7+0+0=7] PilotSeaVehicle                                                                                   
                                             [7+0+0=7] Riding                                                                                            
    
Cyberware:
    Auditory System [1/1]                 Internal Cyberware [1/7]     Shoulders [1/2]           
        Cyberaudio Suite [500eb] [2/3]        Toxin Binders [100eb]        Big Knucks [100eb]    
            Radio Communicator [100eb]                                                           
            Level Damper [100eb]                                                                 
    
Armor:                                                   Ranged weapons:                                                                                                  
    Head: Light Armorjack [100eb (premium), SP=11/11]        Chadran Arms "Jungle Reaper" (Assault Rifle) [500eb (expensive), standard, Damage=5d6, ROF=1, Mag=/25 ()]    
    Body: Light Armorjack [100eb (premium), SP=11/11]    Melee weapons:                                                                                                   
                                                             Big Knucks [100eb (premium), Damage=2d6, ROF=2]                                                              
                                                             Boxing [Damage=2d6, ROF=1]                                                                                   

Inventory:
    Ammo                                               Equipment / Drugs                                     Junk                                                                        
        [1] Grenades (Incendiary) [100eb (premium)]        [1] Anti-Smog Breathing Mask [20eb (everyday)]        [477] Eddies [1eb (cheap)]                                              
        [50] Bullets (Basic) [1eb (cheap)]                 [1] Flashlight [20eb (everyday)]                      [1] Autographed Photograph of Night City Celebrity [20eb (everyday)]    
                                                           [1] Personal CarePak [20eb (everyday)]                [1] Pipe [20eb (everyday)]                                              
                                                                                                                 [1] Rock                                                                
                                                                                                                 [1] Napkin from nightclub with a phone number on it                     
  ```

</details>

<details>
  <summary>General (Adam Smasher)</summary>
  Input:

  ```
cp_red_npc_generator.exe --rank=general --role=solo
  ```

Output:

  ```
Solo, General, seed=1718139863
Has items total worth of 22842

Health (you can add conditions here):
	HP: 50/50 (Seriously Wounded: 25)

Stats: (stat+modifiers=total)
	[8] INT | [8-4=4] REF | [8-4=4] DEX | [7] TECH | [8] COOL | [8] WILL | [8] LUCK | [8-4=4] MOVE | [8+2=10] BODY | [0] EMP

Skills (stat+skill+modifiers=total):
    Education                             Technique                                Social                            Body                                 
        [8+0+0=8] Accounting                  [7+0+0=7] AirVehicleTech                 [8+0+0=8] Bribery                 [4+3+0=7] Athletics              
        [8+0+0=8] AnimalHandling              [7+0+0=7] BasicTech                      [0+3+0=3] Conversation            [4+0+0=4] Contortionist          
        [8+0+0=8] Bureaucracy                 [7+0+0=7] Cybertech                      [0+3+0=3] HumanPerception         [4+0+0=4] Dance                  
        [8+0+0=8] Business                    [7+0+0=7] Demolitions                    [8+8+0=16] Interrogation          [8+0+0=8] Endurance              
        [8+0+0=8] Composition                 [7+0+0=7] ElectronicsSecurityTech        [8+3+0=11] Persuasion             [8+8+2=18] ResistTortureDrugs    
        [8+0+0=8] Criminology                 [7+8+0=15] FirstAid                      [8+0+0=8] PersonalGrooming        [4+3+0=7] Stealth                
        [8+0+0=8] Cryptography                [7+0+0=7] Forgery                        [8+0+0=8] Streetwise          Awareness                            
        [8+0+0=8] Deduction                   [7+0+0=7] LandVehicleTech                [8+0+0=8] Trading                 [8+3+0=11] Concentration         
        [8+3+0=11] Education                  [7+0+0=7] PaintDrawSculpt                [8+0+0=8] WardrobeStyle           [8+0+0=8] ConcealRevealObject    
        [8+0+0=8] Gamble                      [7+0+0=7] Paramedic                  Fighting                              [8+0+0=8] LipReading             
        [8+0+0=8] LibrarySearch               [7+0+0=7] PhotographyFilm                [4+3+0=7] Brawling                [8+8+0=16] Perception            
        [8+3+0=11] LocalExpertYourHome        [7+0+0=7] PickLock                       [4+8+0=12] Evasion                [8+0+0=8] Tracking               
        [8+8+0=16] Tactics                    [7+0+0=7] PickPocket                     [4+0+0=4] MartialArts         Ranged_Weapon                        
        [8+0+0=8] WildernessSurvival          [7+0+0=7] SeaVehicleTech                 [4+8+0=12] MeleeWeapon            [4+0+0=4] Archery                
        [8+3+0=11] LanguageStreetslang        [7+0+0=7] Weaponstech                    [4+0+3=7] Initiative              [4+8+0=12] Autofire              
        [8+0+0=8] Science                 Control                                  Performance                           [4+8+0=12] Handgun               
                                              [4+0+0=4] DriveLandVehicle               [8+0+0=8] Acting                  [4+0+0=4] HeavyWeapons           
                                              [4+0+0=4] PilotAirVehicle                [7+0+0=7] PlayInstrument          [4+8+0=12] ShoulderArms          
                                              [4+0+0=4] PilotSeaVehicle                                                                                   
                                              [4+0+0=4] Riding                                                                                            
    
Cyberware:
    Shoulders [2/2]                              Internal Cyberware [5/7]                     Auditory System [1/1]                 
        Cyberarm [500eb] [4/4]                       Grafted Muscle and Bone Lace [1000eb]        Cyberaudio Suite [500eb] [3/3]    
            Popup Ranged Weapon (SMG) [500eb]        Enhanced Antibodies [500eb]                      Radio Communicator [100eb]    
            Popup Grenade Launcher [500eb]           Radar / Sonar Implant [1000eb]                   Radar Detector [500eb]        
        Cyberarm [500eb] [4/4]                       Toxin Binders [100eb]                            Level Damper [100eb]          
            Popup Shield [500eb]                     Independent Air Supply [1000eb]          Hips [2/2]                            
            Big Knucks [100eb]                   Eye Sockets [2/2]                                Cyberleg [100eb] [2/3]            
    Neuralware [1/1]                                 Cybereye [100eb] [1/3]                           Jump Booster [500eb]          
        Neural Link [500eb] [1/5]                        Anti-Dazzle [100eb]                      Cyberleg [100eb] [2/3]            
            Sandevistan [500eb]                      Cybereye [100eb] [1/3]                           Jump Booster [500eb]          
    Fashionware [1/7]                                    Anti-Dazzle [100eb]                                                        
        Biomonitor [100eb]                                                                                                          
    
Armor:                                             Ranged weapons:                                                                                   
    Head: Metalgear [5000eb (luxury), SP=18/18]        Popup Grenade Launcher [500eb (expensive), Damage=6d6, ROF=1, Mag=/2 ()]                      
    Body: Metalgear [5000eb (luxury), SP=18/18]        Militech "Viper" (Heavy SMG) [500eb (expensive), excellent, Damage=3d6, ROF=1, Mag=/40 ()]    
    Popup Shield [500eb (expensive), SP=10/10]         Popup Ranged Weapon (SMG) [500eb (expensive), Damage=2d6, ROF=1, Mag=/30 ()]                  
                                                   Melee weapons:                                                                                    
                                                       Big Knucks [100eb (premium), Damage=2d6, ROF=2]                                               
                                                       Boxing [Damage=3d6, ROF=1]                                                                    

Inventory:
    Ammo                                                   Equipment / Drugs                             Junk                                     
        [2] Grenades (Armor-Piercing) [100eb (premium)]        [2] Berserker [100eb (premium)]               [2725] Eddies [1eb (cheap)]          
        [2] Grenades (Flashbang) [100eb (premium)]             [2] Timewarp [100eb (premium)]                [1] Hygiene Bag [10eb (cheap)]       
        [80] Bullets (Basic) [1eb (cheap)]                     [2] Black Lace [50eb (costly)]                [1] Area Streetmap [10eb (cheap)]    
                                                               [1] Handcuffs [50eb (costly)]                 [1] Vape-Pen [10eb (cheap)]          
                                                               [1] Airhypo [50eb (costly)]                   [1] Zip Ties                         
                                                               [1] Flashlight [20eb (everyday)]                                                   
                                                               [1] Personal CarePak [20eb (everyday)]                                             
                                                               [1] Synthcoke [20eb (everyday)]                                                    
  ```

</details>

## Limitations (or todos? who knows)

* No complex modifiers, only +N to stats/skills (for ex. 3 tattoos won't give you +2 Personal Grooming)
* No complex requirements, only containers (for ex. I disabled Beta/Sigma Frames generation as they require 2/1 Grafted
  Muscle and Bone Lace)
* No skill chips
* Skills - only upgrades to street rat
* (Almost) only items from the basic rulebook
* No weapon modifications
* No exotic weapons
