#!/usr/bin/env python3

'''
wizardry_monster_id.py - infers actual monsters from results from one encounter (kill counts, experience points)
Copyright (C) 2023 github user bassjack1 <147515670+bassjack1@users.noreply.github.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Communication with the author can be done via tagging @bassjack1 in github.com issues or by composing
private messages to user bassjack1 on reddit.com : https://www.reddit.com/message/compose/
'''

'''
Global comments and general description:
This program is designed to be used for the Apple ][ version of Wizardry, and for the first scenario "Proving Grounds
of the Mad Overlord". It will not give accurate results for other scenarios/versions.

This program uses and relies on data and explanations from user Ahab who posted on blogspot.com several pages about the
apple ][ version of wizardry : https://datadrivengamer.blogspot.com/2019/08/game-85-wizardry-proving-grounds-of-mad.html

Special Thanks to Ahab

Explanation of use:
This is a command line program written in the Python programming language, which is widely available as a free download
for many computer operating systems. It was developed on a computer running Linux, with Python version 3.7.7 installed.

Example execution with arguments:

% wizardry_monster_id.py 5pri 1mil 1176x
 - 1 master thief (lo)
 - 5 lvl 5 priest

In the example, the user input indicates that in a single encounter 5 PRIESTS and 1 MAN IN LEATHER were killed and each
survivor in the party was given 1176 experience points. (by default, the party size is assumed to be 6 - see usage)
The output of the program shows that based on the experience points awarded the program has inferred that the 5
PRIESTS were actually LVL 5 PRIESTS, and the MAN IN LEATHER was actually a MASTER THIEF (and since there are 3
monster entities with name "MASTER THIEF" the suffix "(lo)" indicates that the lower level variety of master thief
was what was involved.)

This program requires the presence of these two data files in the working directory:
- monsters.json
- unidentified_groups.json

monsters.json file format
[
  {"key": "amh", "key_name": "arch mage (hi)", "game_name": "ARCH MAGE", "group_key": "mir",  "image_index": 7, "xp": 3160, "co_occur_keys": ["hw"]},
  {"key": "aml", "key_name": "arch mage (lo)", "game_name": "ARCH MAGE", "group_key": "mir",  "image_index": 7, "xp": 790, "co_occur_keys": ["cs"]},
  {"key": "ad", "key_name": "attack dog", "game_name": "ATTACK DOG", "group_key": "ani",  "image_index": 11, "xp": 1120, "co_occur_keys": ["df"]},
  ...
]

this json list contains monster objects with these fields:
- key : a short unique string to refer to a particular monster (such as "b" for "BISHOP")
- key_name : the full name of the monster as it will be output when the exact monsters are determined (such as 'bishop')
- game_name : the name of the identified monster in wizardry (such as "BISHOP")
- group_key : a short unique string to link to the appropriate unidentified group in wizardry (such as "pri" for "PRIEST")
- image_index : an integer representing an image displayed when the monster is encountered (such as 8)
- xp : the number of xp awarded for each such monster killed in combat (such as 1135)
- co_occur_keys : a list of monster keys (usually only one) indicating the potential co-occuring monster should this monster come with additional allies

The picture integers:
0 SLIME
1 SMALL HUMANOID
2 SKELETON
3 MAN IN LEATHER
4 MAN IN CHAIN
5 WEIRD HUMANOID
6 GAS CLOUD
7 MAN IN ROBES
8 PRIEST
9 MAN IN KIMONO
10 BEAR
11 ANIMAL
12 AMPHIBIAN
13 FLY
14 INSECT
15 DRAGON
16 GIANT
17 DEMON
18 TREASURE CHEST (never a monster in this wizardry scenario/version)
19 coins (can be "creeping coins?")

unidentified_groups.json file format is simplified from the monsters.json file format
[
  {"key": "amp", "key_name": "amphibian", "game_group": "AMPHIBIAN"},
  {"key": "ani", "key_name": "animal", "game_group": "ANIMAL"},
  {"key": "bea", "key_name": "bear", "game_group": "BEAR"},
  ...
]

special cases:
--
monster MASTER NINJA standardized to be in unidentified group "MAN IN ROBES" (from "MAN IN ROBE")
monster HIGH NINJA standardized to be in unidentified group "KIMONOED MAN" (from "MAN IN KIMONO")
--
There are 4 cases where the unidentified group name may be the same as an identified group name:
- unidentified group GARGOYLE must be the monster of the same name
- unidentified group GAS CLOUD must be the monster of the same name
- unidentified group OGRE may be the monster of the same name, or may be OGRE LORD
- unidentified group WERERAT must be the monster of the same name
Because of this, users will get the same result whether they use unidentified group codes gar/gas/wer
(GARGOYLE/GAS CLOUD/WERERAT) or the known monster codes g/gc/wr (GARGOYLE/GAS CLOUD/WERERAT)
However, users probably should only use unidentified group code ogr for encountered OGRE groups.
Only if they are certain that they were not fighting OGRE LORD can they reliably use the
known monster code og (OGRE).
--
Some known monster names occur in the game monster table multiple times leading to some ambiguity:
MASTER THIEF occurs three times, with 4HitDice (960xp), 6HD (1140xp), and 12HD (1935xp).
  In the output, these are suffixed with (lo), (mid), and (hi) to distinguish them and they
  can trigger co-occurence of LVL 5 PRIEST 10% for (lo), ARCH MAGE (lo) 25% for (mid), and 100% LVL 8 FIGHTER (hi).
ARCH MAGE occurs twice, with 8HD and SpellLevel 2 (790xp), and 20HD and SL 6 (3160xp).
  In the output, these are suffixed with (lo), and (hi) to distinguish them and they
  can trigger co-occurence of CHAMP SAMURAI 30% for (lo), and HIGH WIZARD 100% for (hi).
HIGH PRIEST occurs three times, with 8HD (2160xp), 11HD (3300xp), and 8HD (2200xp)
  In the output, these are suffixed with (lo), (hi), and (sp) to distinguish them and they
  can trigger co-occurence of CHAMP SAMURAI 20% for (lo), and FIRE GIANT 100% for (hi), and 100% HIGH NINJA for (sp).
  The (sp) case only occurs as part of the unique encounter within the monster allocation center.
HUGE SPIDER occurs twice. Both occurrences have the same stats and xp, but differ in the
  possible triggered co-occurence monsters. The first occurs commonly on level 4 and 5 and
  has BORING BEETLE 10% cooccurrence. The other occurs commonly on level 5 and has SHADE 10%.
  Both have been represented as a single monster which may trigger one of two cooccurences.
LVL 7 MAGE occurs three times, all with 7HD, and with SL 4 (1000xp), SL 5 (1240xp), and SL 4 (1000xp).
  In the output the second case (SL 5) is suffixed with (hi), and the other two (represented as a single monster) are suffixed with "(lo)/(sp)".
  The (lo)/(sp) case does occur as part of the unique encounter within the monster allocation center -
  during that encounter, the triggered co-occurrence monster is HIGH PRIEST (sp) 100%. In other encounters,
  the (lo)/(sp) case triggers co-occurence of LVL 6 NINJA 20%. The (hi) case triggers co-occurence of
  WYVERN 30%.
These somewhat ambiguous co-occurence relationships have been verified:
  - CHAMP SAMURAI trigger HIGH PRIEST (lo) [instead of HIGH PRIEST (hi)]
  - CHIMERA trigger ARCH MAGE (lo) [instead of ARCH MAGE (hi)]
  - LVL 6 NINJA trigger MASTER THIEF (lo) [instead of (mid) or (hi)]
  - MASTER NINJA trigger LVL 7 MAGE (hi) [instead of (lo)/(sp)]
  - MASTER THIEF (mid) trigger ARCH MAGE (lo) [instead of (hi)]
  - RAVER LORD trigger HIGH PRIEST (hi) [instead of (lo) or (sp)]
  - BORING BEETLE and GIANT SPIDER both trigger HUGE SPIDER ... and
        in particular, trigger the HUGE SPIDER which may trigger BORING BEETLE (not the one which may trigger SHADE)

Inescapable ambiguity:
with multiple unidentified monster groups and the right combination of kill counts, there will
be cases which are truly ambiguous. For instance, if a user defeated
4 priests, 6 men in robes, 3 men in armor, 7 strange animals, and was awarded 6050 xp per character
in a 6 character party (example user input : 4pri6mir3mia7sa6050x6c),
all of these assignments of particular monsters would be satisfactory:
- 6 hatamoto (6 * 1600xp), 7 trolls (7 * 1720xp), 4 lvl 8 bishops (4 * 2060xp), 3 lvl 8 fighters (3 * 2140xp)
- 6 arch mage (lo) (6 * 790xp), 7 gorgons (7 * 2920xp), 4 lvl 8 bishops (4 * 2060xp), 3 swordsmen (3 * 960xp)
- 6 lvl 7 mage (hi) (7 * 1240xp), 7 gaze hounds (7 * 1235xp), 4 high priests [higher] (4 * 3300xp), 3 major daimyos (3 * 2340xp)
The first 2 cases total to 36300 xp  and the last one totals to 36305 .. all of which equal 6050 when you divide by 6 and drop fractions.
Potentially, the monster picture (shown for the first group of monsters in the encounter) might disambiguate.
(The images for trolls, gorgons, and gaze hounds all differ even though they are all "Strange Animals", but
hatamotos, arch mages, and lvl 7 mages all use the same image. Behavior in battle may also help (spells cast).)
Some of these cases (such as the example above) will never occur. If you examine which monsters can
possibly co-occur, any encounter with gaze hounds will only include gaze hounds (no other monsters)
so assignment 3 is not possible. Similarly, enounters which include trolls will only include other trolls
or must include an ogre lord. So assignment 1 is not possible. Assignment 2 is more plausible, but
when arch mages are present, they must co-occur only with {High Wizard, Champ Samurai, Master Thief, Chimera}
so assignment 2 is actually not possible either.
An acutal case which occurred in practice was the encounter in the monster allocation center (example
user input : 2pri2mir1kim1600x5c), had two valid outputs based on the experience points being split
between 5 surviving party members:
 - 1 lvl 3 ninja (1360xp), 2 hatamoto (2 * 1600xp), 2 lvl 8 priest (2 * 1720xp)
 - 1 high ninja (1600xp), 2 lvl 7 mage (lo)/(sp) (2 * 1000xp), 2 high priest (sp) (2 * 2200xp)
Both cases total to 8000xp. (To be honest, the game informed on the actual identity of
the high ninja immediately and all monsters by the end of the encounter, but it makes an illustrative case)

Co-occurrence problems:
Some of the monsters in an unidentified group trigger co-occurence of other monsters in that group.
When that happens, the player may only know that a certain number with a group name were killed but
not how many from each distinct duplicate group. Example : 3 small humanoids (actually orcs) and
5 small humanoids (actually kobolds) are encountered. In the first round two small humanoids flee before
makanito eliminates all monsters. User will not know whether both of the fleeing monsters fled from
the same group, or what group/groups they fled from. They will only know that a total of 6 small humanoids
were killed. To find the solution, the program would need to explore all divisions of the 6 small humanoids
into two subgroups (possible future improvement). With insects, there can be three different monsters of type
insect encountered at once (in up to 4 INSECT groups). Here are all actual trigger paths:
ani : dragon puppy, killer wolf (KW->DP) [observed]
ins : boring beetle, giant spider, huge spider (BB->HS) (HS->BB) (GS->HS->BB)
kim : lvl 1 ninja, lvl 3 ninja (L3N->L1N) [observed]
mir : hatamoto, lvl 10 mage, lvl 7 mage (lo)/(sp), master ninja, arch mage (lo), arch mage (hi), high wizard
        (H->L10M) (L10M->gg->ch->AML) (MN->L7ML) (AMH->HW)
pri : lvl 1 priest, lvl 3 priest (L3p->L1p)
sa : chimera, gorgon (GG->CH)
sh : kobold, orc (K->O) (O->K) [observed]
sli : bubbly slime, creeping crud (CC->BS)
ue : grave mist, shade, vampire, vampire lord (GM->S) (S->rc->GM) [observed] (VL->V)
There is a case of double multi occurence where a LVL 10 MAGE triggers the occurence of a GORGON which
triggers the occurence of a CHIMERA which triggers the occurence of an ARCH MAGE (LO). If all of these
monsters are unidentified there will be four groups : two groups with name "MAN IN ROBES" (one of which will
be mages and the other of which will be wizards), and two groups with name "STRANGE ANIMAL" (one of which
will be gorgons and the other of which will be chimeras)
Some of these cases may be handled by making educated guesses about the counts of the actual monsters
killed and using the program to verify the validity of those guesses.
'''

import json
import re
import string
import sys

class InvalidKeyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class MissingKeyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class DuplicateKeyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class MonsterGroup:
    def __init__(self, dup_group_count, total_monster_count, group_code):
        self.dup_group_count = dup_group_count
        self.total_monster_count = total_monster_count
        sef.group_code = group_code

def show_usage():
    sys.stdout.write('wizardry_monster_id.py  Copyright (C) 2023 github user bassajack1\n')
    sys.stdout.write('This program comes with ABSOLUTELY NO WARRANTY\n')
    sys.stdout.write('This is free software, and you are welcome to redistribute it\n')
    sys.stdout.write('under certain conditions; see file LICENSE (GPL 3) for details.\n')
    sys.stdout.write('\n')
    sys.stdout.write('Usage: (may require prefixing with your python3 executable)\n')
    sys.stdout.write('wizardry_monster_id.py [TERM ...] XP_TERM \n')
    sys.stdout.write('      infers actual monsters killed based on encounter details.\n')
    sys.stdout.write('      Each provided TERM must be of the form <count><code>\n')
    sys.stdout.write('      where code is a recognized monster code or unidentified\n')
    sys.stdout.write('      group code (see "codes" option below) or is special code\n')
    sys.stdout.write('      "c" to indicate how many of your party characters ended\n')
    sys.stdout.write('      the encounter in a non-disabled state (default: 6)\n')
    sys.stdout.write('      XP_TERM uses sepecial code "x" to indicate experience\n')
    sys.stdout.write('      points given "TO EACH SURVIVOR".\n')
    sys.stdout.write('      Otherwise, all counts should specify the total of each\n')
    sys.stdout.write('      monster type killed (excluding those dissoved or fled).\n')
    sys.stdout.write('      Note: whitespace between TERMs is optional\n')
    sys.stdout.write(' wizardry_monster_id.py codes\n')
    sys.stdout.write('      shows unidentified group code and monster code lists\n')
    sys.stdout.write(' wizardry_monster_id.py groups\n')
    sys.stdout.write('      shows detailed information about all unidentified groups\n')
    sys.stdout.write('      such as possible monsters in groups and ambiguities.\n')

def user_is_asking_for_help(first_arg):
    return first_arg in {'help', '--help', 'usage', '--usage', '?', '/?'}

def read_obj_list_from_file(filename, file_description, list_ref):
    with open(filename, 'r') as file:
        file_content = json.load(file)
    for obj in file_content:
        key = obj["key"]
        if key == "_comment":
            continue
        list_ref.append(obj)

def construct_key_map(key_map, object_list):
    for obj in object_list:
        if "key" not in obj:
            msg = 'expected a dictionary entry for "key" but not found in object : %s\n' % (str(obj))
            raise MissingKeyError(msg)
        if obj["key"] in key_map:
            msg = "error : encountered a second object with key '%s' : %s\n" % (obj["key"], str(obj))
            raise DuplicateKeyError(msg)
        key_map[obj["key"]] = obj

def construct_unidentified_group_to_monster_map(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map):
    for group_key in unidentified_group_map:
        unidentified_group_to_monster_set_map[group_key] = set()
    for monster_key in monster_map:
        monster = monster_map[monster_key]
        group_key = monster["group_key"]
        if group_key in unidentified_group_to_monster_set_map:
            monster_set = unidentified_group_to_monster_set_map[group_key]
            monster_set.add(monster_key)
        else:
            sys.stderr.write("Error : unidentified group key %s for monster key %s not covered in groups file\n" % (group_key, monster_key))

'''
valid keys begin with a letter and contain no whitespace
also, the keys "x" and "c" are reserved for experience points and character count respectively
'''
def key_is_valid(key):
    if key.lower() in ["x", "c"]:
        return False
    valid_key_re = re.compile("^[A-Za-z]\\S*$")
    return valid_key_re.match(key) != None

def validate_keys(map_with_keys, source_filename):
    for key in map_with_keys:
        if not key_is_valid(key):
            msg = "while reading file %s, an invalid key string '%s' was encountered\n" % (source_filename, key)
            raise InvalidKeyError(msg)

def write_out_monster_codes_and_unidentified_group_codes(monster_map, unidentified_group_map):
    sys.stdout.write('Note that there are several cases where the same in-game monster name string is used for multiple distinct monster types.\n')
    sys.stdout.write('In these cases, it may be advisable to use a code corresponding to the unidentified group rather than the exact monster.\n')
    sys.stdout.write('The first column contains the code to be used as input to this program.\n')
    sys.stdout.write('The second column contains "g" for an unidentified group entity or "m" for a monster entity.\n')
    sys.stdout.write('The third column contains the in-game text used for the entity (caps) followed by this program\'s output text for monsters (lower).\n')
    sys.stdout.write('This program always uses the singular form for entity names (e.g. "MAN IN BLACK" rather than "MEN IN BLACK")\n')
    sys.stdout.write('In-game text "MAN IN ROBE" and "MAN IN KIMONO" changed to "MAN IN ROBES" and "KIMONOED MAN" respectively in this program.\n')
    sys.stdout.write("\n")
    sys.stdout.write("Codes for unidentified group entities and monster entities:\n")
    for group_key in sorted(unidentified_group_map):
        unidentified_group = unidentified_group_map[group_key]
        sys.stdout.write("  %6s" % (unidentified_group["key"]))
        sys.stdout.write(" g")
        sys.stdout.write(" %s" % (unidentified_group["game_group"]))
        sys.stdout.write("\n")
    for monster_key in sorted(monster_map):
        monster = monster_map[monster_key]
        sys.stdout.write("  %6s" % (monster["key"]))
        sys.stdout.write(" m")
        sys.stdout.write(" %s %s" % (monster["game_name"],monster["key_name"]))
        sys.stdout.write("\n")

def write_out_unidentified_group_and_monsters(group_key, monster_map, unidentified_group_to_monster_set_map):
    sys.stdout.write("%4s :" % (group_key))
    first = True
    for monster_key in sorted(unidentified_group_to_monster_set_map[group_key]):
        if not first:
            sys.stdout.write(",")
        else:
            first = False
        monster = monster_map[monster_key]
        sys.stdout.write(" %s" % (monster["key_name"]))
    sys.stdout.write("\n")

def write_out_unidentified_groups_with_only_one_monster(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map):
    sys.stdout.write("groups with only one monster:\n")
    for group_key in unidentified_group_to_monster_set_map:
        if len(unidentified_group_to_monster_set_map[group_key]) == 1:
            write_out_unidentified_group_and_monsters(group_key, monster_map, unidentified_group_to_monster_set_map)

def write_out_unidentified_groups_with_several_monsters(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map):
    sys.stdout.write("\ngroups with more than one monster:\n")
    for group_key in unidentified_group_to_monster_set_map:
        if len(unidentified_group_to_monster_set_map[group_key]) > 1:
            write_out_unidentified_group_and_monsters(group_key, monster_map, unidentified_group_to_monster_set_map)

def find_all_monster_tuples_of_monster(monster_key, produced_monster_tuple_set, monster_map):
    in_progress_monster_tuple_list = []
    in_progress_monster_tuple_list.append([monster_key])
    while in_progress_monster_tuple_list:
        in_progress_monster_tuple = in_progress_monster_tuple_list.pop(0)
        if len(in_progress_monster_tuple) == 4:
            # 4 groups is a completed tuple
            produced_monster_tuple_set.add(",".join(in_progress_monster_tuple))
            continue
        last_monster_key = in_progress_monster_tuple[-1]
        co_occur_keys = monster_map[last_monster_key]["co_occur_keys"]
        if len(co_occur_keys) == 0:
            # nothing else can be added
            produced_monster_tuple_set.add(",".join(in_progress_monster_tuple))
            continue
        for co_occur_key in co_occur_keys:
            new_tuple = []
            for key in in_progress_monster_tuple:
                new_tuple.append(key)
            new_tuple.append(co_occur_key)
            in_progress_monster_tuple_list.append(new_tuple)

def capitalize_group_in_tuple(monster_tuple, capitalized_group_key, monster_map):
    new_monster_key_list = []
    for monster_key in monster_tuple.split(","):
        group_key = monster_map[monster_key]["group_key"]
        if group_key == capitalized_group_key:
            new_monster_key_list.append(monster_key.upper())
        else:
            new_monster_key_list.append(monster_key)
    return ",".join(new_monster_key_list)

def find_multi_occurring_groups_of_tuple(monster_tuple, multi_occurring_group_to_produced_tuple_list_map, monster_map):
    group_key_to_count = {}
    monster_key_already_seen = set()
    for monster_key in monster_tuple.split(","):
        if monster_key in monster_key_already_seen:
            continue
        monster_key_already_seen.add(monster_key)
        group_key = monster_map[monster_key]["group_key"]
        if group_key in group_key_to_count:
            group_key_to_count[group_key] += 1
        else:
            group_key_to_count[group_key] = 1
    for group_key in group_key_to_count:
        if group_key_to_count[group_key] > 1:
            capitalized_tuple = capitalize_group_in_tuple(monster_tuple, group_key, monster_map)
            if group_key in multi_occurring_group_to_produced_tuple_list_map:
                multi_occurring_group_to_produced_tuple_list_map[group_key] += "\n\t" + capitalized_tuple
            else:
                multi_occurring_group_to_produced_tuple_list_map[group_key] = "\t" + capitalized_tuple

def is_capitalized(string):
    return string == string.upper()

def convert_monster_keys_to_monster_key_names(produced_tuple_list, monster_map, unidentified_group_map):
    named_monster_tuple_list_set = set()
    lines = produced_tuple_list.split('\n')
    for line in lines:
        if line.startswith('\t'):
            line = line[1:]
        first_member_index = -1
        last_member_index = -1
        monster_name_list = []
        monster_key_list = line.split(',')
        for index, monster_key in enumerate(monster_key_list):
            monster_key_name = monster_map[monster_key.lower()]["key_name"]
            if is_capitalized(monster_key):
                if first_member_index == -1:
                    first_member_index = index
                last_member_index = index
                monster_name_list.append(monster_key_name.upper())
            else:
                monster_name_list.append(monster_key_name)
        named_monster_tuple_list_set.add(", ".join(monster_name_list[first_member_index:last_member_index + 1]))
    return "\t" + "\n\t".join(sorted(named_monster_tuple_list_set))

def write_out_multi_occurring_unidentified_groups(monster_map, unidentified_group_map):
    sys.stdout.write("\ngroups which can multi-occur (group members capitalized):\n")
    produced_monster_tuple_set = set()
    for monster_key in monster_map:
        find_all_monster_tuples_of_monster(monster_key, produced_monster_tuple_set, monster_map)
    multi_occurring_group_to_produced_tuple_list_map = {}
    for monster_tuple in sorted(produced_monster_tuple_set):
        find_multi_occurring_groups_of_tuple(monster_tuple, multi_occurring_group_to_produced_tuple_list_map, monster_map)
    for group_key in sorted(multi_occurring_group_to_produced_tuple_list_map):
        produced_tuple_list = multi_occurring_group_to_produced_tuple_list_map[group_key]
        named_monster_tuple_list = convert_monster_keys_to_monster_key_names(produced_tuple_list, monster_map, unidentified_group_map)
        sys.stdout.write("%4s: \n%s\n" % (group_key, named_monster_tuple_list))

def write_out_unidentified_groups_and_possible_monsters_for_each(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map):
    write_out_unidentified_groups_with_only_one_monster(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map)
    write_out_unidentified_groups_with_several_monsters(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map)
    write_out_multi_occurring_unidentified_groups(monster_map, unidentified_group_map)

def find_next_matching_key(remainder, entity_map):
    longest_match = ""
    for key in entity_map:
        if remainder.startswith(key):
            if len(key) > len(longest_match):
                longest_match = key
    if len(longest_match) > 0:
        return longest_match
    else:
        return None

def write_code_list(code_map):
    remaining_entity_count = len(code_map)
    for key in code_map:
        entity = code_map[key]
        if remaining_entity_count > 1:
            sys.stderr.write("%s " % key)
        else:
            sys.stderr.write("%s" % key)
        remaining_entity_count -= 1

def write_expected_input(monster_map, unidentified_group_map):
    sys.stderr.write("expected input format is one or more <int><code> pairs (example: 3wh)\n")
    sys.stderr.write("<int> should be the number of monsters killed (not including those which flee or dissolve) or xp/characters\n")
    sys.stderr.write("unidentified monster group codes (see unidentified_groups.json):\n")
    sys.stderr.write("  ")
    write_code_list(unidentified_group_map)
    sys.stderr.write("\n")
    sys.stderr.write("identified monster codes (see monsters.json):\n")
    sys.stderr.write("  ")
    write_code_list(monster_map)
    sys.stderr.write("\n")
    sys.stderr.write("special codes:\n")
    sys.stderr.write("  x (for experience points awarded per character)\n")
    sys.stderr.write("  c (for number of non-incapacitated characters at encounter end)\n")

def find_next_number(s, monster_map, unidentified_group_map):
    number_re = re.compile("^([0-9]+)")
    match = number_re.match(s)
    if match == None:
        if len(s) == 0:
            s = "<end_of_input>"
        sys.stderr.write("error : could not find expected number at this position in input '%s'\n" % s)
        write_expected_input(monster_map, unidentified_group_map)
        sys.exit(1)
    number = match.groups()[0]
    return number

def find_next_number_key_pair(s, monster_map, unidentified_group_map):
    number = find_next_number(s, monster_map, unidentified_group_map)
    remainder = s[len(number):]
    special_keys = {"x": "experience points", "c": "character count"}
    key = find_next_matching_key(remainder, unidentified_group_map)
    if not key:
        key = find_next_matching_key(remainder, monster_map)
    if not key:
        key = find_next_matching_key(remainder, special_keys)
    if not key:
        if len(remainder) == 0:
            remainder = "<end of input>"
        sys.stderr.write("error : could not find expected monster key or unidentified group key at this position in input '%s'\n" % remainder)
        write_expected_input(monster_map, unidentified_group_map)
        sys.exit(1)
    return number, key

'''
function to parse a single string into groups with monster counts
format example : 7wol5wer4ani2703x6c - means 7 wolves killed, 5 wererats killed, 4 animals killed,
2703 experience points awarded per character, 6 characters in non-disabled condition
'''
def parse_groups_from_input(userstring, monster_map, unidentified_group_map):
    # all fields of input are number/key pairs. 7wol5wer4ani2100x6c is 7wol 5wer 4ani 2100x 6c. However, the keys can have digits in them.
    s = userstring
    parsed_query = {}
    while len(s) > 0:
        number, key = find_next_number_key_pair(s, monster_map, unidentified_group_map)
        if key in parsed_query:
            parsed_query[key] = str(int(parsed_query[key]) + int(number))
        else:
            parsed_query[key] = number
        s = s[len(number) + len(key):]
    if not "x" in parsed_query:
        sys.stdout.write("error : it is required that the input include the earned experience points, such as '2100x'\n")
        sys.stdout.write("running this program with no arguments will print a description of usage.\n")
        sys.exit(1)
    if not "c" in parsed_query:
        parsed_query["c"] = 6 # default to a full party if not specified
    return parsed_query

def map_minus_key(basis_map, subtracted_key):
    result_map = {}
    for key in basis_map:
        if not key == subtracted_key:
            result_map[key] = basis_map[key]
    return result_map

def compute_total_xp(deduced_monster_map, monster_map):
    total_xp = 0
    for key in deduced_monster_map:
        if key in monster_map:
            total_xp += int(monster_map[key]["xp"]) * int(deduced_monster_map[key])
        else:
            sys.stderr.write("error - some programming error allowed deduced_monster_map to contain a non-recognized key\n")
            sys.exit(1)
    return total_xp

def xp_total_matches_close_enough(usergroups, known_monster_total_xp):
    user_xp = int(usergroups["x"])
    user_character_count = int(usergroups["c"])
    #sys.stderr.write("        user_xp = %s\n" % (str(user_xp)))
    #sys.stderr.write("        user_cc = %s\n" % (str(user_character_count)))
    #sys.stderr.write("        known_monster_total_xp = %s\n" % (str(known_monster_total_xp)))
    #sys.stderr.write("        computed ratio = %s\n" % (str(known_monster_total_xp / user_character_count)))
    return int(known_monster_total_xp / user_character_count) == user_xp

def recursively_search_unidentified_groups_for_satisfactory_monster_maps(
            usergroups,
            user_unidentified_group_map,
            monster_map,
            unidentified_group_map,
            unidentified_group_to_monster_set_map,
            known_monster_total_xp):
    #sys.stderr.write("entered rsugfsmm with user_unid_group_map %s\n" % (str(user_unidentified_group_map)))
    if len(user_unidentified_group_map) == 0:
        #sys.stderr.write("    testing xp compatibility (ug=%s, totalxp=%s).." % (str(usergroups), str(known_monster_total_xp)))
        if xp_total_matches_close_enough(usergroups, known_monster_total_xp):
            # xp requrement was satisfied .. return an object to represent this case
            return [ {} ]
        else:
            return []
    found_satisfactory_monster_maps = []
    # iterate over one unkown group
    selected_unidentified_group = next(iter(user_unidentified_group_map.keys()))
    #sys.stderr.write("selected group : %s\n" % (selected_unidentified_group))
    for possible_monster in unidentified_group_to_monster_set_map[selected_unidentified_group]:
        #sys.stderr.write("  possible monster is: %s\n" % (possible_monster))
        adjusted_total_xp = known_monster_total_xp + monster_map[possible_monster]["xp"] * int(usergroups[selected_unidentified_group])
        #sys.stderr.write("  adjusted xp : %s\n" % (adjusted_total_xp))
        adjusted_user_unidentified_group_map = map_minus_key(user_unidentified_group_map, selected_unidentified_group)
        satisfactory_monster_maps_for_choice = recursively_search_unidentified_groups_for_satisfactory_monster_maps(
                usergroups,
                adjusted_user_unidentified_group_map,
                monster_map,
                unidentified_group_map,
                unidentified_group_to_monster_set_map,
                adjusted_total_xp)
        for satisfactory_monster_map in satisfactory_monster_maps_for_choice:
            satisfactory_monster_map[possible_monster] = usergroups[selected_unidentified_group]
        found_satisfactory_monster_maps += satisfactory_monster_maps_for_choice
    return found_satisfactory_monster_maps

'''
XP of all known monster groups are totalled and deducted from the user specified xp, yielding an xp total for the unidentified groups.
All permutations of possible monster selection from each unidentified group is attempted and a list of all valid assignments (which capture the xp total) are collected and returned.
An example to test the combination of groups which are the same monster would be : 6sh6o470x6c or 6sh6sh470x6c
'''
def deduce_monsters_from_usergroups(usergroups, monster_map, unidentified_group_map, unidentified_group_to_monster_set_map):
    known_monster_total_xp = 0
    known_monster_map = {}
    user_unidentified_group_map = {}
    for key in usergroups:
        if key == "x":
            continue
        if key == "c":
            continue
        if key in unidentified_group_map:
            user_unidentified_group_map[key] = usergroups[key]
            continue
        if key in monster_map:
            known_monster_map[key] = usergroups[key]
            known_monster_total_xp = int(known_monster_total_xp) + int(monster_map[key]["xp"]) * int(usergroups[key])
        else:
            sys.stderr.write("error - some programming error allowed usergroups to contain a non-recognized key\n")
            sys.exit(1)
    deduced_monster_map_list = [ {} ] # default for when there are no unidentified groups
    if len(user_unidentified_group_map) > 0:
        deduced_monster_map_list = recursively_search_unidentified_groups_for_satisfactory_monster_maps(
                usergroups,
                user_unidentified_group_map,
                monster_map,
                unidentified_group_map,
                unidentified_group_to_monster_set_map,
                known_monster_total_xp)
    # add in the known monsters
    for deduced_monster_map in deduced_monster_map_list:
        for known_monster in known_monster_map:
            if known_monster in deduced_monster_map:
                deduced_monster_map[known_monster] = str(int(deduced_monster_map[known_monster]) + int(known_monster_map[known_monster]))
            else:
                deduced_monster_map[known_monster] = known_monster_map[known_monster]
    # report case if xp requirements are not satisfied (only happens when all monsters were known)
    cases_to_skip_in_output = []
    for deduced_monster_map in deduced_monster_map_list:
        computed_total_xp = compute_total_xp(deduced_monster_map, monster_map)
        if not xp_total_matches_close_enough(usergroups, computed_total_xp):
            sys.stderr.write("The xp computation for this case does not match what was computed from the monster counts.\n")
            sys.stderr.write("This case will not be output:\n\t%s\n" % str(deduced_monster_map))
            cases_to_skip_in_output.append(deduced_monster_map)
    return_list = []
    for deduced_monster_map in deduced_monster_map_list:
        if not deduced_monster_map in cases_to_skip_in_output:
            return_list.append(deduced_monster_map)
    return return_list

'''
spaces will be ignored ... so collapse all command line arguments into a single string
'''
def construct_user_query(args):
    joined_args = ""
    for arg in args[1:]:
        joined_args += "".join(arg.split())
    return joined_args

def output_entity_term(key, count, monster_map, unidentified_group_map, user_value_flag):
    if user_value_flag:
        sys.stdout.write("[input] ")
    if key in unidentified_group_map:
        sys.stdout.write(" - %s %s\n" % (count, unidentified_group_map[key]["key_name"]))
    else:
        sys.stdout.write(" - %s %s\n" % (count, monster_map[key]["key_name"]))

def output_entities_from_map(entity_map, monster_map, unidentified_group_map, user_value_flag):
    for key in entity_map:
        if key == "x" or key == "c":
            continue
        count = entity_map[key]
        output_entity_term(key, count, monster_map, unidentified_group_map, user_value_flag)

def output_xp_and_character_count(usergroups):
    xp = usergroups["x"]
    character_count = usergroups["c"]
    sys.stdout.write("[input] (%s experience points for" % (xp))
    sys.stdout.write(" %s characters)\n" % (character_count))

def output_user_input(usergroups, monster_map, unidentified_group_map):
    output_entities_from_map(usergroups, monster_map, unidentified_group_map, True)
    output_xp_and_character_count(usergroups)

def output_deduced_monster_assignment(monster_map, unidentified_group_map, deduced_monster_assignment):
    output_entities_from_map(deduced_monster_assignment, monster_map, unidentified_group_map, False)

'''
If only one assignment gives the correct total, output all mosters with counts and xp contribution.
If zero or more than one assignment gives the correct total, output the situation to user
'''
def output_deduced_monster_assignments(usergroups, monster_map, unidentified_group_map, deduced_monster_assignments):
    if len(deduced_monster_assignments) == 0:
        sys.stdout.write("Could not find identification for:\n")
        output_user_input(usergroups, monster_map, unidentified_group_map)
        sys.exit(0)
    if len(deduced_monster_assignments) > 1:
        sys.stdout.write("More than one selection of specific monsters yields the correct xp total. Perhaps examine the first monster group, the rendered image, and the potential co-spawners. All valid selections:\n")
    for deduced_monster_assignment in deduced_monster_assignments:
        output_deduced_monster_assignment(monster_map, unidentified_group_map, deduced_monster_assignment)
        if len(deduced_monster_assignments) > 1:
            sys.stdout.write("----------------------------------------\n")

def main():
    unidentified_groups = []
    monsters = []
    unidentified_group_map = {}
    monster_map = {}
    read_obj_list_from_file('unidentified_groups.json', "unidentified groups", unidentified_groups)
    read_obj_list_from_file('monsters.json', "monsters", monsters)
    construct_key_map(unidentified_group_map, unidentified_groups)
    construct_key_map(monster_map, monsters)
    validate_keys(monster_map, "monsters.json")
    validate_keys(unidentified_group_map, "unidentified_groups.json")
    unidentified_group_to_monster_set_map = {}
    construct_unidentified_group_to_monster_map(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map)
    if len(sys.argv) == 1 or user_is_asking_for_help(sys.argv[1]):
            show_usage()
            return
    if sys.argv[1] == "codes":
            write_out_monster_codes_and_unidentified_group_codes(monster_map, unidentified_group_map)
            return
    if sys.argv[1] == "groups":
            write_out_unidentified_groups_and_possible_monsters_for_each(monster_map, unidentified_group_map, unidentified_group_to_monster_set_map)
            return
    else:
        userstring = construct_user_query(sys.argv)
        usergroups = parse_groups_from_input(userstring, monster_map, unidentified_group_map)
        deduced_monster_assignments = deduce_monsters_from_usergroups(usergroups, monster_map, unidentified_group_map, unidentified_group_to_monster_set_map)
        output_deduced_monster_assignments(usergroups, monster_map, unidentified_group_map, deduced_monster_assignments)

if __name__ == "__main__":
    main()
