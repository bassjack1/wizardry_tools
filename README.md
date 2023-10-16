# wizardry_tools

Tools for use with the computer game "Wizardry"

## License
All tools released under GNU GPL v3.0 : See [LICENSE](./LICENSE)

## wizardry_monster_id.py
This program infers actual monsters killed based on encounter details.

This program is designed to be used for the Apple \]\[ version of Wizardry, and for the first scenario "Proving Grounds
of the Mad Overlord". It will not give accurate results for other scenarios/versions.

This program uses and relies on data and explanations from user Ahab who
[posted](https://datadrivengamer.blogspot.com/2019/08/game-85-wizardry-proving-grounds-of-mad.html) on blogspot.com
several pages about the apple \]\[ version of wizardry.

Special Thanks to Ahab

Explanation of use:
This is a command line program written in the Python programming language, which is widely available as a free download
for many computer operating systems. It was developed on a computer running Linux, with Python version 3.7.7 installed.

Example execution with arguments:

```
% wizardry_monster_id.py 5pri 1mil 1176x
 - 1 master thief (lo)
 - 5 lvl 5 priest
```

In the example, the user input indicates that in a single encounter 5 PRIESTS and 1 MAN IN LEATHER were killed and each
survivor in the party was given 1176 experience points. (by default, the party size is assumed to be 6 - see usage)
The output of the program shows that based on the experience points awarded the program has inferred that the 5
PRIESTS were actually LVL 5 PRIESTS, and the MAN IN LEATHER was actually a MASTER THIEF (and since there are 3
monster entities with name "MASTER THIEF" the suffix "(lo)" indicates that the lower level variety of master thief
was what was involved.)

This program requires the presence of these two data files in the working directory:
- [monsters.json](./monsters.json)
- [unidentified\_groups.json](./unidentified_groups.json)

Usage:
```
wizardry_monster_id.py [TERM ...] XP_TERM
      infers actual monsters killed based on encounter details.
      Each provided TERM must be of the form <count><code>
      where code is a recognized monster code or unidentified
      group code (see "codes" option below) or is special code
      "c" to indicate how many of your party characters ended
      the encounter in a non-disabled state (default: 6)
      XP_TERM uses sepecial code "x" to indicate experience
      points given "TO EACH SURVIVOR".
      Otherwise, all counts should specify the total of each
      monster type killed (excluding those dissoved or fled).
      Note: whitespace between TERMs is optional
 wizardry_monster_id.py codes
      shows unidentified group code and monster code lists
 wizardry_monster_id.py groups
      shows detailed information about all unidentified groups
      such as possible monsters in groups and ambiguities.
```

See comments in the code for fuller explanations and details about ambiguities and limitations.
