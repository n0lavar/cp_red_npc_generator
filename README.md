# Cyberpunk Red NPC generator

[![Donate](https://img.shields.io/badge/Donate-8A2BE2)](https://revolut.me/n0lavar)

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

## Info

A generator that generates NPCs based on json configs using the specified rank and role.

Generated:

* Stats

  Stats are generated based on the list of stats for each role for a street rat from the rulebook: a random set is
  selected and scaled according to the rank. The lowest rank has a stat sum of 45, the highest has a stat sum of 80.

* Skills

  Skills are generated based on the list of skills for the role for a street rat from the rulebook: the list is taken
  and scaled according to rank. The lowest rank has a skill sum of 50, the highest has a skill sum of 110.

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
usage: main.py [-h] --rank
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

## Example of input and output data

Input:

```
python cp_red_npc_generator/src/main.py --rank=general --role=solo
```

Output:

```
Solo, General, seed=1717444140
Has items total worth of 28122

Health (you can add conditions here):
    HP: 50/50 (Seriously Wounded: 25)

Stats: (stat + modifiers = total)
    [8] INT | [8-4=4] REF | [8-4=4] DEX | [6] TECH | [8] COOL | [8] WILL | [8] LUCK | [8-4=4] MOVE | [8+2=10] BODY | [1] EMP

Skills (stat + skill + modifiers = total):
    Education                             Technique                                Social                            Body                                 
        [8+0+0=8] Accounting                  [6+0+0=6] AirVehicleTech                 [8+0+0=8] Bribery                 [4+3+0=7] Athletics              
        [8+0+0=8] AnimalHandling              [6+0+0=6] BasicTech                      [1+3+0=4] Conversation            [4+0+0=4] Contortionist          
        [8+0+0=8] Bureaucracy                 [6+0+0=6] Cybertech                      [1+3+0=4] HumanPerception         [4+0+0=4] Dance                  
        [8+0+0=8] Business                    [6+0+0=6] Demolitions                    [8+8+0=16] Interrogation          [8+0+0=8] Endurance              
        [8+0+0=8] Composition                 [6+0+0=6] ElectronicsSecurityTech        [8+3+0=11] Persuasion             [8+8+2=18] ResistTortureDrugs    
        [8+0+0=8] Criminology                 [6+8+0=14] FirstAid                      [8+0+0=8] PersonalGrooming        [4+3+0=7] Stealth                
        [8+0+0=8] Cryptography                [6+0+0=6] Forgery                        [8+0+0=8] Streetwise          Awareness                            
        [8+0+0=8] Deduction                   [6+0+0=6] LandVehicleTech                [8+0+0=8] Trading                 [8+3+0=11] Concentration         
        [8+3+0=11] Education                  [6+0+0=6] PaintDrawSculpt                [8+0+0=8] WardrobeStyle           [8+0+0=8] ConcealRevealObject    
        [8+0+0=8] Gamble                      [6+0+0=6] Paramedic                  Ranged_Weapon                         [8+0+0=8] LipReading             
        [8+0+0=8] LibrarySearch               [6+0+0=6] PhotographyFilm                [4+0+0=4] Archery                 [8+8+0=16] Perception            
        [8+3+0=11] LocalExpertYourHome        [6+0+0=6] PickLock                       [4+8+0=12] Autofire               [8+0+0=8] Tracking               
        [8+8+0=16] Tactics                    [6+0+0=6] PickPocket                     [4+8+0=12] Handgun            Fighting                             
        [8+0+0=8] WildernessSurvival          [6+0+0=6] SeaVehicleTech                 [4+0+0=4] HeavyWeapons            [4+3+0=7] Brawling               
        [8+3+0=11] LanguageStreetslang        [6+0+0=6] Weaponstech                    [4+8+0=12] ShoulderArms           [4+8+0=12] Evasion               
        [8+0+0=8] Science                 Control                                  Performance                           [4+0+0=4] MartialArts            
                                              [4+0+0=4] DriveLandVehicle               [8+0+0=8] Acting                  [4+8+0=12] MeleeWeapon           
                                              [4+0+0=4] PilotAirVehicle                [6+0+0=6] PlayInstrument          [4+0+3=7] Initiative             
                                              [4+0+0=4] PilotSeaVehicle                                                                                   
                                              [4+0+0=4] Riding                                                                                            
    
Cyberware:
    Eye Sockets [2/2]                            Borgware                                         Internal Cyberware [5/7]                     
        Cybereye [100eb] [2/3]                       MultiOptic Mount [1000eb] [1/5]                  Radar / Sonar Implant [1000eb]           
            Targeting Scope [500eb]                      Cybereye [100eb] [2/3]                       Toxin Binders [100eb]                    
            Anti-Dazzle [100eb]                              Low Light / Infrared / UV [500eb]        Enhanced Antibodies [500eb]              
        Cybereye [100eb] [3/3]                       Artificial Shoulder Mount [1000eb] [1/2]         Independent Air Supply [1000eb]          
            Anti-Dazzle [100eb]                          Cyberarm [500eb] [3/4]                       Grafted Muscle and Bone Lace [1000eb]    
            Low Light / Infrared / UV [500eb]                Popup Shield [500eb]                 Hips [2/2]                                   
    Shoulders [2/2]                              Neuralware [1/1]                                     Cyberleg [100eb] [2/3]                   
        Cyberarm [500eb] [4/4]                       Neural Link [500eb] [2/5]                            Jump Booster [500eb]                 
            Popup Grenade Launcher [500eb]               Sandevistan [500eb]                          Cyberleg [100eb] [2/3]                   
            Popup Ranged Weapon (SMG) [500eb]            Chipware Socket [500eb] [1/1]                    Jump Booster [500eb]                 
        Big Knucks [100eb]                                   Pain Editor [1000eb]                 Auditory System [1/1]                        
    Fashionware [1/7]                                                                                 Cyberaudio Suite [500eb] [3/3]           
        Biomonitor [100eb]                                                                                Level Damper [100eb]                 
                                                                                                          Radio Communicator [100eb]           
                                                                                                          Radar Detector [500eb]               
    
Armor:                                             Weapons:                                                                                                     
    Head: Metalgear [5000eb (luxury), SP=18/18]        Big Knucks [100eb (premium), Damage=2d6, ROF=2]                                                          
    Body: Metalgear [5000eb (luxury), SP=18/18]        Militech "Dragon" (Assault Rifle) [1000eb (very_expensive), excellent, Damage=5d6, ROF=1, Mag=/25 ()]    
    Popup Shield [500eb (expensive), SP=10/10]         Popup Ranged Weapon (SMG) [500eb (expensive), Damage=2d6, ROF=1, Mag=/30 ()]                             
                                                       Boxing [Damage=3d6, ROF=1]                                                                               
                                                       Popup Grenade Launcher [500eb (expensive), Damage=6d6, ROF=1, Mag=/2 ()]                                 

Inventory:
    Ammo                                                Equipment / Drugs                             Junk                               
        [60] Bullets (Basic) [1eb (cheap)]                  [1] Carryall [20eb (everyday)]                [2012] Eddies [1eb (cheap)]    
        [30] Bullets (Armor-Piercing) [10eb (cheap)]        [1] Airhypo [50eb (costly)]                   [1] An old coin                
        [2] Grenades (Smoke) [50eb (costly)]                [1] Flashlight [20eb (everyday)]              [1] Paper Letter               
                                                            [1] Handcuffs [50eb (costly)]                 [1] SafeLok combination        
                                                            [1] Personal CarePak [20eb (everyday)]        [1] Broken Metal Fangs         
                                                            [2] Timewarp [100eb (premium)]                                               
```

## Limitations

* No complex modifiers, only +N to stats/skills
* No skill chips
* Skills - only upgrades to street rat
* (Almost) only items from the basic rulebook
* No weapon modifications
* No exotic weapons
