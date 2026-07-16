# NPC generator

An unofficial generator for use with Cyberpunk RED.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
![lines](https://sloc.xyz/github/n0lavar/cp_red_npc_generator?category=code)
![lines](https://sloc.xyz/github/n0lavar/cp_red_npc_generator?category=comments)
![lines](https://sloc.xyz/github/n0lavar/cp_red_npc_generator?category=effort)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/cw/n0lavar)

## Info

A generator that generates NPCs based on json configs using the specified rank and role.  
See `configs/ranks.xlsx` for balance details.

Generates:

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
2. Download `npc_generator_for_cp_red.zip` and unpack it. The archive contains the executable, the `configs` directory,
   and a ready-to-edit `settings.json` in the same directory as the executable.
3. Open Explorer where the `npc_generator_for_cp_red.exe` file is, type "cmd" in the address bar and press Enter.
4. Now you should see a command prompt opened in the right directory where you can type commands from examples.  
   Try this for starters: `npc_generator_for_cp_red.exe --rank=captain --role=solo`.

Calling `npc_generator_for_cp_red.exe` without arguments generates a captain-rank solo.

<details>
  <summary>Full <code>-h</code> output</summary>

```text
usage: npc_generator_for_cp_red.exe [-h]
               [--rank {private,corporal,lieutenant,captain,lieutenant_colonel,lieutenant_general,general,0,1,2,3,4,5,6}]
               [--role {rockerboy,solo,netrunner,tech,medtech,media,exec,lawman,fixer,nomad,civilian}]
               [--nationality {en_US,es_MX,ja_JP,zh_CN,ru_RU,vi_VN,es_CO,pt_BR,ko_KR,id_ID,en_AU,es_AR,de_DE,en_GB,en_PH,fil_PH,tl_PH,es_CL,en_CA,es_CA,fr_CA,en_PK,fr_FR,uk_UA,it_IT,es_ES,pl_PL,en_IN,gu_IN,hi_IN,mr_IN,or_IN,ta_IN,en_NZ,tr_TR,en_TH,th_TH,nl_NL,ar_EG,zu_ZA,am_ET,pt_PT,bn_BD,en_BD,ne_NP,ro_RO,fa_IR,sv_SE,de_AT,en_KE,cs_CZ,uz_UZ,el_GR,tw_GH,hu_HU,no_NO,ar_SA,fi_FI,bg_BG,az_AZ,ar_AE,he_IL,sk_SK,fr_BE,nl_BE,hr_HR,ka_GE,ar_JO,en_NG,ha_NG,ig_NG,ng_NG,yo_NG,en_IE,ga_IE,lt_LT,hy_AM,da_DK,dk_DK,el_CY,ar_DZ,fr_DZ,lv_LV,sq_AL,de_CH,fr_CH,it_CH,sl_SI,et_EE,ar_PS,mk_MK,mt_MT,is_IS,bs_BA,sr_BA,ar_BH,de_LU,lb_LU,de_LI}]
               [--allow-non-basic-ammo | --no-allow-non-basic-ammo]
               [--allow-grenades | --no-allow-grenades]
               [--allow-armor | --no-allow-armor]
               [--allow-cyberware | --no-allow-cyberware]
               [--allow-borgware | --no-allow-borgware]
               [--allow-drugs | --no-allow-drugs]
               [--allow-equipment | --no-allow-equipment]
               [--allow-money | --no-allow-money]
               [--allow-junk | --no-allow-junk]
               [--allow-melee-weapon | --no-allow-melee-weapon]
               [--allow-ranged-weapon | --no-allow-ranged-weapon]
               [--allow-martial-arts | --no-allow-martial-arts] [--seed SEED]
               [--model-id MODEL_ID] [--model-api-key MODEL_API_KEY]
               [--model-base-url MODEL_BASE_URL]
               [--model-language MODEL_LANGUAGE] [--flat | --no-flat]
               [--foundry-json | --no-foundry-json]
               [--log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]

options:
  -h, --help            show this help message and exit

NPC Customization:
  --rank {private,corporal,lieutenant,captain,lieutenant_colonel,lieutenant_general,general,0,1,2,3,4,5,6}
                        A measure of the development of a given NPC, where
                        private is an unskilled and unknown newcomer, and
                        general is a world-class character. Rank determines
                        how advanced an NPC's skills are and how cool his
                        equipment is.
  --role {rockerboy,solo,netrunner,tech,medtech,media,exec,lawman,fixer,nomad,civilian}
                        An occupation the NPC is known by on The Street.
                        `civilian` means that this is just a regular human.
                        The role can determine the equipment and the direction
                        of the NPC's skills. The default value is `solo`.
  --nationality {en_US,es_MX,ja_JP,zh_CN,ru_RU,vi_VN,es_CO,pt_BR,ko_KR,id_ID,en_AU,es_AR,de_DE,en_GB,en_PH,fil_PH,tl_PH,es_CL,en_CA,es_CA,fr_CA,en_PK,fr_FR,uk_UA,it_IT,es_ES,pl_PL,en_IN,gu_IN,hi_IN,mr_IN,or_IN,ta_IN,en_NZ,tr_TR,en_TH,th_TH,nl_NL,ar_EG,zu_ZA,am_ET,pt_PT,bn_BD,en_BD,ne_NP,ro_RO,fa_IR,sv_SE,de_AT,en_KE,cs_CZ,uz_UZ,el_GR,tw_GH,hu_HU,no_NO,ar_SA,fi_FI,bg_BG,az_AZ,ar_AE,he_IL,sk_SK,fr_BE,nl_BE,hr_HR,ka_GE,ar_JO,en_NG,ha_NG,ig_NG,ng_NG,yo_NG,en_IE,ga_IE,lt_LT,hy_AM,da_DK,dk_DK,el_CY,ar_DZ,fr_DZ,lv_LV,sq_AL,de_CH,fr_CH,it_CH,sl_SI,et_EE,ar_PS,mk_MK,mt_MT,is_IS,bs_BA,sr_BA,ar_BH,de_LU,lb_LU,de_LI}
                        Faker locale used to generate the NPC name, e.g. ru_RU
                        or en_US. If omitted, a random nationality is used.
  --allow-non-basic-ammo, --no-allow-non-basic-ammo
                        Is specified, allow non-basic ammo, such as armor
                        piercing and expansive.
  --allow-grenades, --no-allow-grenades
                        Is specified, allow grenades
  --allow-armor, --no-allow-armor
                        Is specified, allow armor items (cyberware armor will
                        still be there).
  --allow-cyberware, --no-allow-cyberware
                        Is specified, allow cyberware.
  --allow-borgware, --no-allow-borgware
                        If specified, allow borgware. Usually you don't want
                        the regular mooks to use that cool stuff.
  --allow-drugs, --no-allow-drugs
                        Is specified, allow adding drugs. Drugs may be added
                        or not depending on airhypo generation.
  --allow-equipment, --no-allow-equipment
                        Is specified, allow equipment, such as flashlight and
                        airhypo (cyberware equipment will still be there).
  --allow-money, --no-allow-money
                        Is specified, allow money.
  --allow-junk, --no-allow-junk
                        Is specified, allow useless junk for flavor.
  --allow-melee-weapon, --no-allow-melee-weapon
                        Is specified, allow melee weapon (brawling, martial
                        arts and cyberware weapons will still be there).
  --allow-ranged-weapon, --no-allow-ranged-weapon
                        Is specified, allow ranged weapon (cyberware weapons
                        will still be there).
  --allow-martial-arts, --no-allow-martial-arts
                        Is specified, allow martial arts (brawling will still
                        be there).

Generation settings:
  --seed SEED           A number for a random engine. The same seed will
                        always give the same result when the other arguments
                        are unchanged. The default is 0, which means "use unix
                        epoch".
  --model-id MODEL_ID   Model identifier used to generate the NPC description.
  --model-api-key MODEL_API_KEY
                        API key for the OpenAI-compatible model server.
  --model-base-url MODEL_BASE_URL
                        Base URL of the OpenAI-compatible model server.
  --model-language MODEL_LANGUAGE
                        Language in which the model generates the NPC
                        description.

Appearance:
  --flat, --no-flat     If specified, don't use columns. Easier for editing
                        and copy-pasting, but takes much more space.
  --foundry-json, --no-foundry-json
                        If specified, output results in JSON format that is
                        suitable for Foundry VVT.
  --log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Logging level. Default is INFO.
```

</details>

Every Boolean option has a positive and negative form. Command-line arguments override values loaded from
`settings.json`.

## settings.json

The release archive contains `settings.json` beside `npc_generator_for_cp_red.exe`. Edit this file to save
defaults instead of repeating arguments on every run. When running from source, copy the repository's
`settings.example.json` to `settings.json` first and edit the copy; keep the example unchanged as a reference.

The program looks for `settings.json` in the current directory first, then beside the packaged executable; when run from
source it also checks the repository root.

The file contain one JSON object. Keys may use hyphens (as in CLI options) or underscores. A command-line option always
overrides the corresponding saved value.

```json
{
  "rank": "captain",
  "role": "solo",
  "seed": 42,
  "nationality": "en_US",
  "model_id": null,
  "allow-borgware": false,
  "allow-junk": true
}
```

## Generated identity and description

Normal text output now begins with the generated identity:

```text
Name Surname (en_US, 22 yo)

An optional AI-generated description appears here.

Has items total worth of ...
```

Descriptions use the OpenAI-compatible `POST /chat/completions` API. Defaults target LM Studio:

```console
npc_generator_for_cp_red.exe --rank=captain --role=solo --model-id=... --model-api-key=... --model-base-url=... --model-language=English
```

Replace `...` with the model identifier, API key, and server base URL. The equivalent `settings.json` values are:

```json
{
  "model_id": "qwen/qwen3.6-35b-a3b",
  "model_api_key": "lm-studio",
  "model_base_url": "http://localhost:1234/v1",
  "model_language": "English"
}
```

Set `model_id`, `model_api_key`, or `model_base_url` to `null` to disable AI description generation. The NPC's name,
nationality, sex, and age are generated regardless.

Start the model server before generating an NPC. The NPC and its template are sent to the configured server as JSON; the
system prompt lives in `configs/description_prompt.md`. Connection errors, timeouts, and invalid responses produce an
`AI description was not generated` warning but do not abort NPC generation. The random seed is sent to the model, though
exact repeatability depends on whether the server and model honor it.

## Text output layout

By default, the character sheet uses multiple columns to keep the output compact. Use `--flat` for a single-column
layout that is easier to edit and copy, but takes considerably more vertical space.

## Examples of input and output data

<details>
  <summary>Private (the lowest rank, punching dolls for the initial characters)</summary>
  Input:

```console
npc_generator_for_cp_red.exe --rank=private --role=solo --seed=101 --nationality=en_US --model-id=... --model-api-key=... --model-base-url=... --model-language=English
```

Possible output:

```text
<=================================================================================================>

--rank=private --role=solo --nationality=en_US --allow-non-basic-ammo --allow-grenades --allow-armor --allow-cyberware --no-allow-borgware --allow-drugs --allow-equipment --allow-money --allow-junk --allow-melee-weapon --allow-ranged-weapon --allow-martial-arts --seed=101 --model-id=qwen/qwen3.6-35b-a3b --model-api-key=lm-studio --model-base-url=http://localhost:1234/v1 --model-language=English --no-flat --no-foundry-json --log-level=INFO 
Kevin Lee (en_US, 21 yo)

    A scuffed leather cap pulls low over a tangle of ash-blond hair, casting the eyes in shadow. His frame is lean
    and unremarkable, built for endurance rather than brute force. Clothing consists of a faded tactical vest over a
    plain thermal shirt, paired with scuffed boots and reinforced trousers. The lack of visible cyberware leaves his
    skin pale and unmarked, save for faint calluses on his palms from gripping tools and weapons. He has a quiet,
    watchful presence, often pausing to double-check straps or adjust his grip before speaking. When others are
    tense, he notices first, offering a nod or a practical suggestion without fanfare. His face is plain but alert,
    with a sharp jawline softened by a habit of chewing his lower lip when processing information. He speaks in
    measured tones, preferring to listen and map out contingencies rather than dominate a room. In the neon-drenched
    sprawl, he blends into the background, a survivor who trusts preparation over bravado and keeps his guard
    perpetually raised.

Has items total worth of 282eb

Stats:          Conditions:                                                   
    [4] INT         HP: 25/25 (Seriously Wounded: 13)                         
    [4] REF         TraumaTeam status: NONE                                   
    [3] DEX         Can evade bullets: False                                  
    [2] TECH        No intangible obscurement penalties: False                
    [3] COOL        Has flashes of light protection: False                    
    [3] WILL        Has ears protection: False                                
    [4] LUCK        Has breath protection: True (Anti-Smog Breathing Mask)    
    [3] MOVE                                                                  
    [3] BODY                                                                  
    [3] EMP                                                                   

Skills:
    Education                               Technique                                  Social                                  
        [4(INT)=4] Accounting                   [2(TECH)=2] AirVehicleTech                 [3(COOL)=3] Bribery                 
        [4(INT)=4] AnimalHandling               [2(TECH)=2] BasicTech                      [3(EMP)+2=5] Conversation           
        [4(INT)=4] Bureaucracy                  [2(TECH)=2] Cybertech                      [3(EMP)+2=5] HumanPerception        
        [4(INT)=4] Business                     [2(TECH)=2] Demolitions                    [3(COOL)+3=6] Interrogation         
        [4(INT)=4] Composition                  [2(TECH)=2] ElectronicsSecurityTech        [3(COOL)+2=5] Persuasion            
        [4(INT)=4] Criminology                  [2(TECH)+3=5] FirstAid                     [3(COOL)=3] PersonalGrooming        
        [4(INT)=4] Cryptography                 [2(TECH)=2] Forgery                        [3(COOL)=3] Streetwise              
        [4(INT)=4] Deduction                    [2(TECH)=2] LandVehicleTech                [3(COOL)=3] Trading                 
        [4(INT)+2=6] Education                  [2(TECH)=2] PaintDrawSculpt                [3(COOL)=3] WardrobeStyle           
        [4(INT)=4] Gamble                       [2(TECH)=2] Paramedic                  Body                                    
        [4(INT)=4] LibrarySearch                [2(TECH)=2] PhotographyFilm                [3(DEX)+2=5] Athletics              
        [4(INT)+2=6] LocalExpertYourHome        [2(TECH)=2] PickLock                       [3(DEX)=3] Contortionist            
        [4(INT)+3=7] Tactics                    [2(TECH)=2] PickPocket                     [3(DEX)=3] Dance                    
        [4(INT)=4] WildernessSurvival           [2(TECH)=2] SeaVehicleTech                 [3(WILL)=3] Endurance               
        [4(INT)+2=6] LanguageStreetslang        [2(TECH)=2] Weaponstech                    [3(WILL)+3=6] ResistTortureDrugs    
        [4(INT)=4] Science                  Awareness                                      [3(DEX)+2=5] Stealth                
    Fighting                                    [3(WILL)+2=5] Concentration            Ranged_Weapon                           
        [3(DEX)+2=5] Brawling                   [4(INT)=4] ConcealRevealObject             [4(REF)=4] Archery                  
        [3(DEX)+3=6] Evasion                    [4(INT)=4] LipReading                      [4(REF)+3=7] Autofire               
        [3(DEX)=3] MartialArts                  [4(INT)+3=7] Perception                    [4(REF)+3=7] Handgun                
        [3(DEX)+3=6] MeleeWeapon                [4(INT)=4] Tracking                        [4(REF)=4] HeavyWeapons             
        [4(REF)=4] Initiative               Control                                        [4(REF)+3=7] ShoulderArms           
    Performance                                 [4(REF)=4] DriveLandVehicle                                                    
        [3(COOL)=3] Acting                      [4(REF)=4] PilotAirVehicle                                                     
        [2(TECH)=2] PlayInstrument              [4(REF)=4] PilotSeaVehicle                                                     
                                                [4(REF)=4] Riding                                                              
    
Armor:                                          Ranged weapons:                                                                                      
    Head: Leathers [20eb (everyday), SP=4/4]        [7(S)/7(A)] Militech "Viper" (Heavy SMG) [50eb (costly), poor, Damage=3d6, ROF=1, Mag=/40 ()]    
    Body: Leathers [20eb (everyday), SP=4/4]    Melee weapons:                                                                                       
                                                    [6] Blacksmith hammer (Very Heavy Melee Weapon) [50eb (costly), poor, Damage=4d6, ROF=1]         
                                                    [5] Brawling [Damage=1d6, ROF=2]                                                                 

Inventory:
    Ammo                                                   Equipment / Drugs                                     Junk                                                       
        [1] Grenades (Armor-Piercing) [100eb (premium)]        [1] Anti-Smog Breathing Mask [20eb (everyday)]        [51] Eddies [1eb (cheap)]                              
        [80] Bullets (Basic) [1eb (cheap)]                                                                           [1] Pipe [20eb (everyday)]                             
                                                                                                                     [1] Fortune Cookie (Unopened)                          
                                                                                                                     [1] Old Can                                            
                                                                                                                     [1] Crude drawing on napkin                            
                                                                                                                     [1] Napkin from nightclub with a phone number on it    
                                                                                                                     [1] Class Schedule for Night City University           
                                                                                                                     [1] Used Plane Ticket
```

</details>

<details>
  <summary>Captain (equivalent of the players' starting characters)</summary>
  Input:

```console
npc_generator_for_cp_red.exe --rank=captain --role=solo --seed=102 --nationality=en_US --model-id=... --model-api-key=... --model-base-url=... --model-language=English
```

Possible output:

```text
<=================================================================================================>

--rank=captain --role=solo --nationality=en_US --allow-non-basic-ammo --allow-grenades --allow-armor --allow-cyberware --no-allow-borgware --allow-drugs --allow-equipment --allow-money --allow-junk --allow-melee-weapon --allow-ranged-weapon --allow-martial-arts --seed=102 --model-id=qwen/qwen3.6-35b-a3b --model-api-key=lm-studio --model-base-url=http://localhost:1234/v1 --model-language=English --no-flat --no-foundry-json --log-level=INFO 
Charles Gilbert (en_US, 35 yo)

    A sharp jawline cuts through the grime of the Badlands, framed by a close-cropped fade trimmed to military
    precision. His face carries a polished, almost sculpted attractiveness—high cheekbones, a straight nose, and
    eyes that track movement with unnerving stillness. A faint chrome trim glints along his jawline, part of a Kill
    Display that pulses with a soft, calculating glow. His movement speed is steady and unremarkable, a measured
    pace that never rushes but never lags. His build is lean but dense, built for endurance rather than bulk,
    wrapped in a tailored light armorjack that hugs his frame without sacrificing mobility. The fabric is dark,
    matte, and impeccably maintained, a stark contrast to the rusted sprawl around him. He moves with a fluid,
    economical grace, every step light and deliberate. A heavy bulletproof shield rests against his forearm, its
    surface scarred but clean. His habits betray a restless need to prove himself: he constantly adjusts his collar,
    checks his reflection in polished metal, and watches others with a quiet, measuring intensity, always ready to
    outpace or outmaneuver them in conversation or combat. There’s a sharp, competitive edge to his posture, like a
    coiled spring that never quite relaxes, even when the job is done.

Has items total worth of 2182eb

Stats:          Conditions:                                                   Actions:          Abilities:                 
    [6] INT         HP: 40/40 (Seriously Wounded: 20)                             Black Lace        Appetite Controller    
    [7] REF         TraumaTeam status: NONE                                       Synthcoke         Handcuffs              
    [7] DEX         Can evade bullets: False                                                                               
    [3] TECH        No intangible obscurement penalties: False                                                             
    [8] COOL        Has flashes of light protection: False                                                                 
    [6] WILL        Has ears protection: False                                                                             
    [5] LUCK        Has breath protection: True (Anti-Smog Breathing Mask)                                                 
    [5] MOVE                                                                                                               
    [6] BODY                                                                                                               
    [4] EMP                                                                                                                

Skills:
    Education                               Technique                                  Social                                   
        [6(INT)=6] Accounting                   [3(TECH)=3] AirVehicleTech                 [8(COOL)=8] Bribery                  
        [6(INT)=6] AnimalHandling               [3(TECH)=3] BasicTech                      [4(EMP)+2=6] Conversation            
        [6(INT)=6] Bureaucracy                  [3(TECH)=3] Cybertech                      [4(EMP)+2=6] HumanPerception         
        [6(INT)=6] Business                     [3(TECH)=3] Demolitions                    [8(COOL)+6=14] Interrogation         
        [6(INT)=6] Composition                  [3(TECH)=3] ElectronicsSecurityTech        [8(COOL)+2=10] Persuasion            
        [6(INT)=6] Criminology                  [3(TECH)+6=9] FirstAid                     [8(COOL)=8] PersonalGrooming         
        [6(INT)=6] Cryptography                 [3(TECH)=3] Forgery                        [8(COOL)=8] Streetwise               
        [6(INT)=6] Deduction                    [3(TECH)=3] LandVehicleTech                [8(COOL)=8] Trading                  
        [6(INT)+2=8] Education                  [3(TECH)=3] PaintDrawSculpt                [8(COOL)=8] WardrobeStyle            
        [6(INT)=6] Gamble                       [3(TECH)=3] Paramedic                  Body                                     
        [6(INT)=6] LibrarySearch                [3(TECH)=3] PhotographyFilm                [7(DEX)+2=9] Athletics               
        [6(INT)+2=8] LocalExpertYourHome        [3(TECH)=3] PickLock                       [7(DEX)=7] Contortionist             
        [6(INT)+6=12] Tactics                   [3(TECH)=3] PickPocket                     [7(DEX)=7] Dance                     
        [6(INT)=6] WildernessSurvival           [3(TECH)=3] SeaVehicleTech                 [6(WILL)=6] Endurance                
        [6(INT)+2=8] LanguageStreetslang        [3(TECH)=3] Weaponstech                    [6(WILL)+6=12] ResistTortureDrugs    
        [6(INT)=6] Science                  Awareness                                      [7(DEX)+2=9] Stealth                 
    Fighting                                    [6(WILL)+2=8] Concentration            Ranged_Weapon                            
        [7(DEX)+2=9] Brawling                   [6(INT)=6] ConcealRevealObject             [7(REF)=7] Archery                   
        [7(DEX)+6=13] Evasion                   [6(INT)=6] LipReading                      [7(REF)+6=13] Autofire               
        [7(DEX)=7] MartialArts                  [6(INT)+6=12] Perception                   [7(REF)+6=13] Handgun                
        [7(DEX)+6=13] MeleeWeapon               [6(INT)=6] Tracking                        [7(REF)=7] HeavyWeapons              
        [7(REF)=7] Initiative               Control                                        [7(REF)+6=13] ShoulderArms           
    Performance                                 [7(REF)=7] DriveLandVehicle                                                     
        [8(COOL)=8] Acting                      [7(REF)=7] PilotAirVehicle                                                      
        [3(TECH)=3] PlayInstrument              [7(REF)=7] PilotSeaVehicle                                                      
                                                [7(REF)=7] Riding                                                               
    
Cyberware:
    Fashionware [2/7]           Internal Cyberware [2/7]               
        Biomonitor [100eb]          Appetite Controller [500eb]        
        Kill Display [100eb]        Bodyweight AutoInjector [100eb]    
    
Armor:                                                   Ranged weapons:                                                                                             
    Head: Light Armorjack [100eb (premium), SP=11/11]        [13] GunMart "Snipe-Star" (Sniper Rifle) [500eb (expensive), standard, Damage=5d6, ROF=1, Mag=/4 ()]    
    Body: Light Armorjack [100eb (premium), SP=11/11]    Melee weapons:                                                                                              
    Bulletproof Shield [100eb (premium), SP=10/10]           [13] Spiked Bat (Heavy Melee Weapon) [100eb (premium), standard, Damage=3d6, ROF=2]                     
                                                             [9] Brawling [Damage=2d6, ROF=2]                                                                        

Inventory:
    Ammo                                                   Equipment / Drugs                                         Junk                                                          
        [1] Grenades (Armor-Piercing) [100eb (premium)]        [1] Bulletproof Shield [100eb (premium), SP=10/10]        [478] Eddies [1eb (cheap)]                                
        [4] Bullets (Armor-Piercing) [10eb (cheap)]            [1] Handcuffs [50eb (costly)]                             [1] Pawnshop Receipt for €$50 Item [50eb (costly)]        
        [16] Bullets (Basic) [1eb (cheap)]                     [1] Black Lace [50eb (costly)]                            [1] Bees (Queen Bee in Cryostasis Box) [50eb (costly)]    
                                                               [1] Anti-Smog Breathing Mask [20eb (everyday)]            [1] Food Stick [10eb (cheap)]                             
                                                               [1] Synthcoke [20eb (everyday)]                           [1] MRE [10eb (cheap)]                                    
                                                                                                                         [1] Glow Stick [10eb (cheap)]                             
                                                                                                                         [1] Scrap of fabric sprayed with perfume/cologne
```

</details>

<details>
  <summary>General (Adam Smasher)</summary>
  Input:

```console
npc_generator_for_cp_red.exe --rank=general --role=solo --seed=103 --nationality=en_US --model-id=... --model-api-key=... --model-base-url=... --model-language=English
```

Possible output:

```text
<=================================================================================================>

--rank=general --role=solo --nationality=en_US --allow-non-basic-ammo --allow-grenades --allow-armor --allow-cyberware --no-allow-borgware --allow-drugs --allow-equipment --allow-money --allow-junk --allow-melee-weapon --allow-ranged-weapon --allow-martial-arts --seed=103 --model-id=qwen/qwen3.6-35b-a3b --model-api-key=lm-studio --model-base-url=http://localhost:1234/v1 --model-language=English --no-flat --no-foundry-json --log-level=INFO 
William Bryant (en_US, 49 yo)

    A jagged scar traces his jawline, disappearing into the stiff collar of a charcoal tactical trench coat. His
    face carries a striking physical attractiveness, all sharp angles and weathered skin, framed by a close-cropped,
    silver-dusted undercut. The eyes are glassy and unblinking, calibrated to scan environments rather than people.
    He wears a reinforced ballistic vest beneath the coat, the heavy fabric stretched taut over a dense, heavily
    muscled physique. His posture is rigid, shoulders squared, movements exceptionally agile and startlingly fast
    when he shifts his weight. Every step covers ground with practiced speed. He checks his gear with methodical
    precision, fingers tapping a steady rhythm against his thigh. When speaking, he cuts straight to the point,
    rarely waiting for others to finish. A faint scowl lingers when conversations drag, and he adjusts his collar
    with a sharp tug whenever the ambient noise spikes. He doesn’t offer comfort; he offers solutions, delivered
    with a cold, unyielding focus. The neon bleed from the street outside catches the polished plating on his
    forearms, where matte-black cybernetics contrast with scarred flesh. A kill counter glows faintly on his wrist,
    ticking upward with quiet indifference.

Has items total worth of 24342eb

Stats:                                             Conditions:                                                                  Actions:           Abilities:                 
    [8] INT                                            HP: 55/55 (Seriously Wounded: No, Pain Editor)                               Sandevistan        Appetite Controller    
    [8-4(Head: Metalgear)=4] REF                       TraumaTeam status: EXECUTIVE                                                 Berserker          Radar Detector         
    [8-4(Head: Metalgear)=4] DEX                       Can evade bullets: False                                                     Black Lace         Radio Communicator     
    [7] TECH                                           No intangible obscurement penalties: True (Low Light / Infrared / UV)        Timewarp           Flashlight             
    [8] COOL                                           Has flashes of light protection: True (Anti-Dazzle)                          Synthcoke          Handcuffs              
    [8] WILL                                           Has ears protection: True (Level Damper)                                                                               
    [7] LUCK                                           Has breath protection: True (Anti-Smog Breathing Mask)                                                                 
    [8-4(Head: Metalgear)=4] MOVE                                                                                                                                             
    [8+2(Grafted Muscle and Bone Lace)=10] BODY                                                                                                                               
    [0] EMP                                                                                                                                                                   

Skills:
    Education                                   Technique                                  Social                                   
        [8(INT)=8] Accounting                       [7(TECH)=7] AirVehicleTech                 [8(COOL)=8] Bribery                  
        [8(INT)=8] AnimalHandling                   [7(TECH)=7] BasicTech                      [0(EMP)+3=3] Conversation            
        [8(INT)=8] Bureaucracy                      [7(TECH)=7] Cybertech                      [0(EMP)+3=3] HumanPerception         
        [8(INT)=8] Business                         [7(TECH)=7] Demolitions                    [8(COOL)+8=16] Interrogation         
        [8(INT)=8] Composition                      [7(TECH)=7] ElectronicsSecurityTech        [8(COOL)+3=11] Persuasion            
        [8(INT)=8] Criminology                      [7(TECH)+8=15] FirstAid                    [8(COOL)=8] PersonalGrooming         
        [8(INT)=8] Cryptography                     [7(TECH)=7] Forgery                        [8(COOL)=8] Streetwise               
        [8(INT)=8] Deduction                        [7(TECH)=7] LandVehicleTech                [8(COOL)=8] Trading                  
        [8(INT)+3=11] Education                     [7(TECH)=7] PaintDrawSculpt                [8(COOL)=8] WardrobeStyle            
        [8(INT)=8] Gamble                           [7(TECH)=7] Paramedic                  Body                                     
        [8(INT)=8] LibrarySearch                    [7(TECH)=7] PhotographyFilm                [4(DEX)+3=7] Athletics               
        [8(INT)+3=11] LocalExpertYourHome           [7(TECH)=7] PickLock                       [4(DEX)=4] Contortionist             
        [8(INT)+8=16] Tactics                       [7(TECH)=7] PickPocket                     [4(DEX)=4] Dance                     
        [8(INT)=8] WildernessSurvival               [7(TECH)=7] SeaVehicleTech                 [8(WILL)=8] Endurance                
        [8(INT)+3=11] LanguageStreetslang           [7(TECH)=7] Weaponstech                    [8(WILL)+8=16] ResistTortureDrugs    
        [8(INT)=8] Science                      Awareness                                      [4(DEX)+3=7] Stealth                 
    Fighting                                        [8(WILL)+3=11] Concentration           Ranged_Weapon                            
        [4(DEX)+2=6] Brawling                       [8(INT)=8] ConcealRevealObject             [4(REF)=4] Archery                   
        [4(DEX)+8=12] Evasion                       [8(INT)=8] LipReading                      [4(REF)+8=12] Autofire               
        [4(DEX)+1=5] MartialArts                    [8(INT)+8=16] Perception                   [4(REF)+8=12] Handgun                
        [4(DEX)+8=12] MeleeWeapon                   [8(INT)=8] Tracking                        [4(REF)=4] HeavyWeapons              
        [4(REF)+3(Sandevistan)=7] Initiative    Control                                        [4(REF)+8=12] ShoulderArms           
    Performance                                     [4(REF)=4] DriveLandVehicle                                                     
        [8(COOL)=8] Acting                          [4(REF)=4] PilotAirVehicle                                                      
        [7(TECH)=7] PlayInstrument                  [4(REF)=4] PilotSeaVehicle                                                      
                                                    [4(REF)=4] Riding                                                               
    
Cyberware:
    Shoulders [2/2]                                   Eye Sockets [2/2]                            Internal Cyberware [5/7]                                   
        Cyberarm [500eb] [4/4]                            Cybereye [100eb] [3/3]                       Grafted Muscle and Bone Lace [1000eb]                  
            Popup Net Launcher [500eb]                        Anti-Dazzle [100eb]                      Internal Body Cyberware Hardened Shielding [1000eb]    
            Modular Finger Cyberhand [100eb] [1/5]            Low Light / Infrared / UV [500eb]        Grafted Muscle and Bone Lace [1000eb]                  
                Airhypo Cyberfinger [100eb]               Cybereye [100eb] [3/3]                       Appetite Controller [500eb]                            
        Cyberarm [500eb] [4/4]                                Anti-Dazzle [100eb]                      Enhanced Antibodies [500eb]                            
            ChainRipp [500eb]                                 Low Light / Infrared / UV [500eb]    Neuralware [1/1]                                           
    Auditory System [1/1]                             Fashionware [2/7]                                Neural Link [500eb] [2/5]                              
        Cyberaudio Suite [500eb] [3/3]                    Biomonitor [100eb]                               Sandevistan [500eb]                                
            Radar Detector [500eb]                        Kill Display [100eb]                             Chipware Socket [500eb] [1/1]                      
            Level Damper [100eb]                                                                               Pain Editor [1000eb]                           
            Radio Communicator [100eb]                                                                                                                        
    
Armor:                                                Ranged weapons:                                                                                                                       
    Head: Metalgear [5000eb (luxury), SP=18/18]           [13(S)/12(A)] Chadran Arms "Jungle Reaper" (Assault Rifle) [1000eb (very_expensive), excellent, Damage=5d6, ROF=1, Mag=/25 ()]    
    Body: Metalgear [5000eb (luxury), SP=18/18]           [12] Popup Net Launcher [500eb (expensive), Damage=0d0, ROF=1, Mag=/1 ()]                                                         
    Bulletproof Shield [100eb (premium), SP=10/10]    Melee weapons:                                                                                                                        
                                                          [5] Aikido (Disarming Combination, Iron Grip) [Damage=3d6, ROF=2]                                                                 
                                                          [13] ChainRipp [500eb (expensive), excellent, Damage=4d6, ROF=1]                                                                  

Inventory:
    Ammo                                                   Equipment / Drugs                                         Junk                                                                        
        [25] Bullets (Expansive) [10eb (cheap)]                [1] Bulletproof Shield [100eb (premium), SP=10/10]        [2920] Eddies [1eb (cheap)]                                             
        [2] Grenades (Armor-Piercing) [100eb (premium)]        [1] Berserker [100eb (premium)]                           [1] Smokeless tobacco (Tin of snuff/chewing tobacco) [50eb (costly)]    
        [2] Net (Net) [50eb (costly)]                          [1] Timewarp [100eb (premium)]                            [1] Pawnshop Receipt for €$50 Item [50eb (costly)]                      
        [25] Bullets (Basic) [1eb (cheap)]                     [1] Handcuffs [50eb (costly)]                                                                                                     
                                                               [1] Black Lace [50eb (costly)]                                                                                                    
                                                               [1] Flashlight [20eb (everyday)]                                                                                                  
                                                               [1] Anti-Smog Breathing Mask [20eb (everyday)]                                                                                    
                                                               [1] Carryall [20eb (everyday)]                                                                                                    
                                                               [1] Synthcoke [20eb (everyday)]
```

</details>

## Limitations (or todos? who knows)

* No skill chips
* Skills - only upgrades to street rat
* (Almost) only items from the basic rulebook
* No weapon modifications
* No exotic weapons

## License

The original source code of this project is licensed under GNU GPLv3.

### Third-party intellectual property

This tool is not intended to replace the Cyberpunk RED Core Rulebook.

Cyberpunk, Cyberpunk RED, Night City, and related names, terminology, game data, and other intellectual property belong
to R. Talsorian Games and/or their respective licensors. Such material is not licensed under GNU GPLv3 by this
repository.

NPC Generator is unofficial content provided under the Homebrew Content Policy of R. Talsorian Games and is not approved
or endorsed by RTG. This content references materials that are the property of R. Talsorian Games and its licensees.
