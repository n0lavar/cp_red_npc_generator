# Cyberpunk Red NPC generator

<a href="https://buymeacoffee.com/n0lavar" target="_blank" title="buymeacoffee">
  <img src="https://iili.io/JIYMmUN.gif"  alt="buymeacoffee-animated-badge" style="width: 160px;">
</a>

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

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
                                [--seed SEED]
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
  Solo, Private, seed=1717841891
  Has items total worth of 112
  
  Health (you can add conditions here):
      HP: 25/25 (Seriously Wounded: 13)
  
  Stats: (stat+modifiers=total)
      [2] INT | [4] REF | [3] DEX | [2] TECH | [3] COOL | [3] WILL | [3] LUCK | [2] MOVE | [3] BODY | [3] EMP
  
  Skills (stat+skill+modifiers=total):
      Education                            Technique                                Social                            Body                                 
          [2+0+0=2] Accounting                 [2+0+0=2] AirVehicleTech                 [3+0+0=3] Bribery                 [3+2+0=5] Athletics              
          [2+0+0=2] AnimalHandling             [2+0+0=2] BasicTech                      [3+2+0=5] Conversation            [3+0+0=3] Contortionist          
          [2+0+0=2] Bureaucracy                [2+0+0=2] Cybertech                      [3+2+0=5] HumanPerception         [3+0+0=3] Dance                  
          [2+0+0=2] Business                   [2+0+0=2] Demolitions                    [3+3+0=6] Interrogation           [3+0+0=3] Endurance              
          [2+0+0=2] Composition                [2+0+0=2] ElectronicsSecurityTech        [3+2+0=5] Persuasion              [3+3+0=6] ResistTortureDrugs     
          [2+0+0=2] Criminology                [2+3+0=5] FirstAid                       [3+0+0=3] PersonalGrooming        [3+2+0=5] Stealth                
          [2+0+0=2] Cryptography               [2+0+0=2] Forgery                        [3+0+0=3] Streetwise          Awareness                            
          [2+0+0=2] Deduction                  [2+0+0=2] LandVehicleTech                [3+0+0=3] Trading                 [3+2+0=5] Concentration          
          [2+2+0=4] Education                  [2+0+0=2] PaintDrawSculpt                [3+0+0=3] WardrobeStyle           [2+0+0=2] ConcealRevealObject    
          [2+0+0=2] Gamble                     [2+0+0=2] Paramedic                  Ranged_Weapon                         [2+0+0=2] LipReading             
          [2+0+0=2] LibrarySearch              [2+0+0=2] PhotographyFilm                [4+0+0=4] Archery                 [2+3+0=5] Perception             
          [2+2+0=4] LocalExpertYourHome        [2+0+0=2] PickLock                       [4+3+0=7] Autofire                [2+0+0=2] Tracking               
          [2+3+0=5] Tactics                    [2+0+0=2] PickPocket                     [4+3+0=7] Handgun             Fighting                             
          [2+0+0=2] WildernessSurvival         [2+0+0=2] SeaVehicleTech                 [4+0+0=4] HeavyWeapons            [3+2+0=5] Brawling               
          [2+2+0=4] LanguageStreetslang        [2+0+0=2] Weaponstech                    [4+3+0=7] ShoulderArms            [3+3+0=6] Evasion                
          [2+0+0=2] Science                Control                                  Performance                           [3+0+0=3] MartialArts            
                                               [4+0+0=4] DriveLandVehicle               [3+0+0=3] Acting                  [3+3+0=6] MeleeWeapon            
                                               [4+0+0=4] PilotAirVehicle                [2+0+0=2] PlayInstrument          [4+0+0=4] Initiative             
                                               [4+0+0=4] PilotSeaVehicle                                                                                   
                                               [4+0+0=4] Riding                                                                                            
      
  Armor:                                          Weapons:                                                                              
      Body: Leathers [20eb (everyday), SP=4/4]        Boxing [Damage=1d6, ROF=1]                                                        
                                                      Arasaka "Minami 10" (SMG) [50eb (costly), poor, Damage=2d6, ROF=1, Mag=/30 ()]    
  
  Inventory:
      Ammo                                      Equipment / Drugs                     Junk                                                  
          [30] Bullets (Basic) [1eb (cheap)]        [1] Carryall [20eb (everyday)]        [37] Eddies [1eb (cheap)]                         
                                                                                          [1] Memory Chip (Personal Data) [10eb (cheap)]    
                                                                                          [1] An old coin                                   
                                                                                          [1] Used Plane Ticket                             
                                                                                          [1] Ashtray [10eb (cheap)]                        
                                                                                          [1] Half-Used Tube of Rouge Noir Lipstick         
                                                                                          [1] NUSA Lapel Pin                                
                                                                                          [1] Broken Eye Implant   
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
  Solo, Captain, seed=1717842137
  Has items total worth of 1792
  
  Health (you can add conditions here):
      HP: 40/40 (Seriously Wounded: 20)
  
  Stats: (stat+modifiers=total)
      [7] INT | [8] REF | [6] DEX | [3] TECH | [6] COOL | [6] WILL | [7] LUCK | [5] MOVE | [6] BODY | [5] EMP
  
  Skills (stat+skill+modifiers=total):
      Education                            Technique                                Social                            Body                                 
          [7+0+0=7] Accounting                 [3+0+0=3] AirVehicleTech                 [6+0+0=6] Bribery                 [6+2+0=8] Athletics              
          [7+0+0=7] AnimalHandling             [3+0+0=3] BasicTech                      [5+2+0=7] Conversation            [6+0+0=6] Contortionist          
          [7+0+0=7] Bureaucracy                [3+0+0=3] Cybertech                      [5+2+0=7] HumanPerception         [6+0+0=6] Dance                  
          [7+0+0=7] Business                   [3+0+0=3] Demolitions                    [6+6+0=12] Interrogation          [6+0+0=6] Endurance              
          [7+0+0=7] Composition                [3+0+0=3] ElectronicsSecurityTech        [6+2+0=8] Persuasion              [6+6+2=14] ResistTortureDrugs    
          [7+0+0=7] Criminology                [3+6+0=9] FirstAid                       [6+0+0=6] PersonalGrooming        [6+2+0=8] Stealth                
          [7+0+0=7] Cryptography               [3+0+0=3] Forgery                        [6+0+0=6] Streetwise          Awareness                            
          [7+0+0=7] Deduction                  [3+0+0=3] LandVehicleTech                [6+0+0=6] Trading                 [6+2+0=8] Concentration          
          [7+2+0=9] Education                  [3+0+0=3] PaintDrawSculpt                [6+0+0=6] WardrobeStyle           [7+0+0=7] ConcealRevealObject    
          [7+0+0=7] Gamble                     [3+0+0=3] Paramedic                  Ranged_Weapon                         [7+0+0=7] LipReading             
          [7+0+0=7] LibrarySearch              [3+0+0=3] PhotographyFilm                [8+0+0=8] Archery                 [7+6+0=13] Perception            
          [7+2+0=9] LocalExpertYourHome        [3+0+0=3] PickLock                       [8+6+0=14] Autofire               [7+0+0=7] Tracking               
          [7+6+0=13] Tactics                   [3+0+0=3] PickPocket                     [8+6+0=14] Handgun            Fighting                             
          [7+0+0=7] WildernessSurvival         [3+0+0=3] SeaVehicleTech                 [8+0+0=8] HeavyWeapons            [6+2+0=8] Brawling               
          [7+2+0=9] LanguageStreetslang        [3+0+0=3] Weaponstech                    [8+6+0=14] ShoulderArms           [6+6+0=12] Evasion               
          [7+0+0=7] Science                Control                                  Performance                           [6+0+0=6] MartialArts            
                                               [8+0+0=8] DriveLandVehicle               [6+0+0=6] Acting                  [6+6+0=12] MeleeWeapon           
                                               [8+0+0=8] PilotAirVehicle                [3+0+0=3] PlayInstrument          [8+0+0=8] Initiative             
                                               [8+0+0=8] PilotSeaVehicle                                                                                   
                                               [8+0+0=8] Riding                                                                                            
      
  Cyberware:
      Auditory System [1/1]                 Internal Cyberware [1/7]     Fashionware [1/7]         
          Cyberaudio Suite [500eb] [1/3]        Toxin Binders [100eb]        Biomonitor [100eb]    
              Level Damper [100eb]                                                                 
      
  Armor:                                                   Weapons:                                                                                                         
      Head: Light Armorjack [100eb (premium), SP=11/11]        Machete (Medium Melee Weapon) [50eb (costly), standard, Damage=2d6, ROF=2]                                   
      Body: Light Armorjack [100eb (premium), SP=11/11]        Boxing [Damage=2d6, ROF=1]                                                                                   
                                                               Chadran Arms "Jungle Reaper" (Assault Rifle) [500eb (expensive), standard, Damage=5d6, ROF=1, Mag=/25 ()]    
  
  Inventory:
      Ammo                                                   Equipment / Drugs                                     Junk                                           
          [50] Bullets (Basic) [1eb (cheap)]                     [1] Handcuffs [50eb (costly)]                         [541] Eddies [1eb (cheap)]                 
          [1] Grenades (Armor-Piercing) [100eb (premium)]        [1] Personal CarePak [20eb (everyday)]                [1] Hair Wax [20eb (everyday)]             
                                                                 [1] Anti-Smog Breathing Mask [20eb (everyday)]        [1] Crude drawing on napkin                
                                                                                                                       [1] Cheap Necklace [20eb (everyday)]       
                                                                                                                       [1] Shell Casing Keychain                  
                                                                                                                       [1] SafeLok combination                    
                                                                                                                       [1] Pack of Breath Mints [10eb (cheap)]    
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
  Solo, General, seed=1717842304
  Has items total worth of 28024
  
  Health (you can add conditions here):
      HP: 50/50 (Seriously Wounded: 25)
  
  Stats: (stat+modifiers=total)
      [8] INT | [8-4=4] REF | [8-4=4] DEX | [4] TECH | [8] COOL | [8] WILL | [8] LUCK | [7-4=3] MOVE | [8+2=10] BODY | [1] EMP
  
  Skills (stat+skill+modifiers=total):
      Education                             Technique                                Social                            Body                                 
          [8+0+0=8] Accounting                  [4+0+0=4] AirVehicleTech                 [8+0+0=8] Bribery                 [4+3+0=7] Athletics              
          [8+0+0=8] AnimalHandling              [4+0+0=4] BasicTech                      [1+3+0=4] Conversation            [4+0+0=4] Contortionist          
          [8+0+0=8] Bureaucracy                 [4+0+0=4] Cybertech                      [1+3+0=4] HumanPerception         [4+0+0=4] Dance                  
          [8+0+0=8] Business                    [4+0+0=4] Demolitions                    [8+8+0=16] Interrogation          [8+0+0=8] Endurance              
          [8+0+0=8] Composition                 [4+0+0=4] ElectronicsSecurityTech        [8+3+0=11] Persuasion             [8+8+2=18] ResistTortureDrugs    
          [8+0+0=8] Criminology                 [4+8+0=12] FirstAid                      [8+0+0=8] PersonalGrooming        [4+3+0=7] Stealth                
          [8+0+0=8] Cryptography                [4+0+0=4] Forgery                        [8+0+0=8] Streetwise          Ranged_Weapon                        
          [8+0+0=8] Deduction                   [4+0+0=4] LandVehicleTech                [8+0+0=8] Trading                 [4+0+0=4] Archery                
          [8+3+0=11] Education                  [4+0+0=4] PaintDrawSculpt                [8+0+0=8] WardrobeStyle           [4+8+0=12] Autofire              
          [8+0+0=8] Gamble                      [4+0+0=4] Paramedic                  Fighting                              [4+8+0=12] Handgun               
          [8+0+0=8] LibrarySearch               [4+0+0=4] PhotographyFilm                [4+3+0=7] Brawling                [4+0+0=4] HeavyWeapons           
          [8+3+0=11] LocalExpertYourHome        [4+0+0=4] PickLock                       [4+8+0=12] Evasion                [4+8+0=12] ShoulderArms          
          [8+8+0=16] Tactics                    [4+0+0=4] PickPocket                     [4+0+0=4] MartialArts         Awareness                            
          [8+0+0=8] WildernessSurvival          [4+0+0=4] SeaVehicleTech                 [4+8+0=12] MeleeWeapon            [8+3+0=11] Concentration         
          [8+3+0=11] LanguageStreetslang        [4+0+0=4] Weaponstech                    [4+0+3=7] Initiative              [8+0+0=8] ConcealRevealObject    
          [8+0+0=8] Science                 Control                                  Performance                           [8+0+0=8] LipReading             
                                                [4+0+0=4] DriveLandVehicle               [8+0+0=8] Acting                  [8+8+0=16] Perception            
                                                [4+0+0=4] PilotAirVehicle                [4+0+0=4] PlayInstrument          [8+0+0=8] Tracking               
                                                [4+0+0=4] PilotSeaVehicle                                                                                   
                                                [4+0+0=4] Riding                                                                                            
      
  Cyberware:
      Eye Sockets [2/2]                            Borgware                                         Internal Cyberware [5/7]                     
          Cybereye [100eb] [2/3]                       MultiOptic Mount [1000eb] [1/5]                  Grafted Muscle and Bone Lace [1000eb]    
              Anti-Dazzle [100eb]                          Cybereye [100eb] [2/3]                       Enhanced Antibodies [500eb]              
              Targeting Scope [500eb]                          Low Light / Infrared / UV [500eb]        Independent Air Supply [1000eb]          
          Cybereye [100eb] [3/3]                       Artificial Shoulder Mount [1000eb] [1/2]         Radar / Sonar Implant [1000eb]           
              Anti-Dazzle [100eb]                          Cyberarm [500eb] [3/4]                       Toxin Binders [100eb]                    
              Low Light / Infrared / UV [500eb]                Popup Shield [500eb]                 Shoulders [2/2]                              
      Neuralware [1/1]                             Auditory System [1/1]                                Cyberarm [500eb] [4/4]                   
          Neural Link [500eb] [2/5]                    Cyberaudio Suite [500eb] [3/3]                       Popup Ranged Weapon (SMG) [500eb]    
              Chipware Socket [500eb] [1/1]                Level Damper [100eb]                             Popup Grenade Launcher [500eb]       
                  Pain Editor [1000eb]                     Radar Detector [500eb]                       Big Knucks [100eb]                       
              Sandevistan [500eb]                          Radio Communicator [100eb]               Hips [2/2]                                   
      Fashionware [1/7]                                                                                 Cyberleg [100eb] [2/3]                   
          Biomonitor [100eb]                                                                                Jump Booster [500eb]                 
                                                                                                        Cyberleg [100eb] [2/3]                   
                                                                                                            Jump Booster [500eb]                 
      
  Armor:                                             Weapons:                                                                                               
      Popup Shield [500eb (expensive), SP=10/10]         Popup Grenade Launcher [500eb (expensive), Damage=6d6, ROF=1, Mag=/2 ()]                           
      Head: Metalgear [5000eb (luxury), SP=18/18]        Big Knucks [100eb (premium), Damage=2d6, ROF=2]                                                    
      Body: Metalgear [5000eb (luxury), SP=18/18]        Boxing [Damage=3d6, ROF=1]                                                                         
                                                         Popup Ranged Weapon (SMG) [500eb (expensive), Damage=2d6, ROF=1, Mag=/30 ()]                       
                                                         Militech "Bulldog" (Shotgun) [1000eb (very_expensive), excellent, Damage=5d6, ROF=1, Mag=/4 ()]    
  
  Inventory:
      Ammo                                                Equipment / Drugs                             Junk                                                    
          [60] Bullets (Basic) [1eb (cheap)]                  [1] Personal CarePak [20eb (everyday)]        [2699] Eddies [1eb (cheap)]                         
          [8] Shotgun Shells (Basic) [1eb (cheap)]            [1] Carryall [20eb (everyday)]                [1] Trans-Anal Exxxpress                            
          [30] Bullets (Armor-Piercing) [10eb (cheap)]                                                      [1] Omamori [10eb (cheap)]                          
          [4] Slugs (Expansive) [10eb (cheap)]                                                              [1] Flask of Expensive Alcohol [100eb (premium)]    
          [20] Slugs (Basic) [1eb (cheap)]                                                                                                                      
          [2] Grenades (Smoke) [50eb (costly)]                                                                                                                  
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
