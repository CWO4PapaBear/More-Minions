# Elemental and Dragonkin first implementation wave

Status: staged handler and audited plan; not compiled, activated or combat-tested. This work is separate from the approved Demon/Undead build.

## Included work

- Drafted a managed-pet-only server handler for ten direct attacks across eight families.
- Added a guarded source integration tool requiring the Demon/Undead rank-selection prerequisite.
- Added a reproducible definition audit with source fingerprints and collision checks.
- Audited all ten against the exported PTR Spell.dbc and spell_dbc IDs: no collisions. Every referenced auxiliary ID exists, but matching row contents and assets still need verification.

| Family | First-wave spells |
|---|---|
| Air Elemental | 892102 Lightning Bolt (Pet) |
| Earth Elemental | 892111 Boulder |
| Fire Elemental | 892121 Fire Blast (Pet) |
| Water Elemental | 892131 Water Bolt (Pet) |
| Black Whelp | 91755 Lesser Fireball, 91758 Fire Blast (Pet) |
| Blue Whelp | 91759 Arcane Bolt |
| Green Whelp | 91821 Acid Spit |
| Red Whelp | 91768 Fireball (Pet), 91819 Fire Blast (Pet) |

## Test-release behavior choices

The handler uses the owning player level for the recovered `$PL` formula, clamped to 1–80. It scales the calculated effect value (including its source dice) before native damage handling, preserving armor, resistance and critical-hit processing. It rounds to the nearest nonnegative integer.

The planned first-release spell_bonus_data entries must explicitly disable additional spell-power/AP coefficients. Shared Ascension scaling passives remain withheld to avoid applying scaling twice. This is a proposed test-release balance policy, not a recovered Ascension server implementation. The handler alone does not install those entries.

Only a managed captured pet with an enabled family mapping, valid capture access and this spell in its eligible family skills may cast the bound imported spell. These are new imported IDs; stock Classic spells are not rebound.

## Remaining gates

1. Compare referenced auxiliary rows, resolve icon/model/visual dependencies and normalize client tooltip formulas (including the malformed Fire Blast expression).
2. Stage and review definition, binding and explicit zero-coefficient SQL plus rollback; obtain fresh proc/binding/bonus collision data.
3. Select and review creature mappings for these eight families.
4. Merge profiles additively, preserving all already-installed families.
5. Build matching client DBC/MPQ updates from the client baseline and compile the server package.
6. Test capture, owner/pet levels, damage, autocast, relog and stable persistence before enabling the mappings.

Periodic damage, healing, walls, triggered skills, crowd-control restrictions and shared scaling passives remain separate follow-on handlers. No unsupported family is enabled by this staging work.

## Validation performed

Python syntax passed. Source staging rejected repeated application and missing prerequisite code. The definition audit rejected a changed spell effect. Native launch-target ordering was checked against the exported core. Full C++ compilation and runtime tests have not run.

The tools are in `tools/staged-elemental-dragonkin`; they write candidates only. Do not copy the draft handler into the current running build or install isolated spell definitions without the remaining gates. Unlike the Demon/Undead mapping package, this wave needs client definitions as well as server work.
