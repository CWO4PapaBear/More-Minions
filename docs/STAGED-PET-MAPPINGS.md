# Staged pet mapping review

**Not active.** Neutral capture eligibility is active; these additional family mappings and stock ability profiles are staged separately.

## Explicit Valley of Trials changes

| Entry | Creature | Family | Creature type | Spawn levels |
| --- | --- | --- | --- | --- |
| 3102 | Felstalker | Felhunter (custom family 110; native family 15) | Demon | Preserve 3–4 |
| 3101 | Vile Familiar | Imp (custom family 115; native family 23) | Change Humanoid to Demon | 1–4 |

Vile Familiar was excluded by the previous type-filtered export. Its complete live template, models and spawn locations must be collected before guarded SQL is finalized. Template changes affect all spawns sharing its entry. Existing spawned creatures may need a respawn/server restart to adopt the new level range. Existing client creature caches may retain the old type until refreshed; no new model or spell asset is required by the template change itself.

## Stock fallback mapping candidates

These candidates passed the exported type, model and basic protection checks. Runtime ownership, friendliness, attackability, level, range, and channel checks still apply. They are not a guarantee of an accessible world spawn. Vile Familiar is the additional explicit override above and is not counted in this 174-row candidate list.

| Entry | Creature | Proposed family | Minimum level |
| --- | --- | --- | --- |
| 7127 | Jaedenar Stalker | Felhunter (Ascension: Felhound) | 1 |
| 7128 | Jaedenar Mana Leech | Felhunter (Ascension: Felhound) | 1 |
| 3102 | Felstalker | Felhunter (Ascension: Felhound) | 3 |
| 17648 | Felhunter Minion | Felhunter (Ascension: Felhound) | 20 |
| 3774 | Felslayer | Felhunter (Ascension: Felhound) | 22 |
| 6071 | Legion Hound | Felhunter (Ascension: Felhound) | 29 |
| 5726 | Jezelle's Felhunter | Felhunter (Ascension: Felhound) | 30 |
| 6268 | Summoned Felhunter | Felhunter (Ascension: Felhound) | 30 |
| 10656 | Guardian Felhunter | Felhunter (Ascension: Felhound) | 30 |
| 4678 | Mana Eater | Felhunter (Ascension: Felhound) | 37 |
| 4681 | Mage Hunter | Felhunter (Ascension: Felhound) | 38 |
| 4685 | Ley Hunter | Felhunter (Ascension: Felhound) | 39 |
| 7767 | Witherbark Felhunter | Felhunter (Ascension: Felhound) | 45 |
| 7125 | Jaedenar Hound | Felhunter (Ascension: Felhound) | 50 |
| 8675 | Felbeast | Felhunter (Ascension: Felhound) | 50 |
| 7126 | Jaedenar Hunter | Felhunter (Ascension: Felhound) | 52 |
| 6010 | Felhound | Felhunter (Ascension: Felhound) | 54 |
| 8668 | Felhound Tracker | Felhunter (Ascension: Felhound) | 54 |
| 9556 | Felhound Minion | Felhunter (Ascension: Felhound) | 54 |
| 10261 | Burning Felhound | Felhunter (Ascension: Felhound) | 54 |
| 17004 | Jir'see | Felhunter (Ascension: Felhound) | 54 |
| 7728 | Kirith the Damned | Felhunter (Ascension: Felhound) | 55 |
| 16950 | Netherhound | Felhunter (Ascension: Felhound) | 58 |
| 17401 | Felhound Manastalker | Felhunter (Ascension: Felhound) | 60 |
| 17540 | Fiendish Hound | Felhunter (Ascension: Felhound) | 60 |
| 19286 | Invading Fel Stalker | Felhunter (Ascension: Felhound) | 60 |
| 20195 | Dagz | Felhunter (Ascension: Felhound) | 60 |
| 19852 | Artifact Seeker | Felhunter (Ascension: Felhound) | 67 |
| 20918 | Deathforge Felstalker | Felhunter (Ascension: Felhound) | 67 |
| 19804 | Hound of the Betrayer | Felhunter (Ascension: Felhound) | 68 |
| 18642 | Fel Guardhound | Felhunter (Ascension: Felhound) | 69 |
| 18605 | Felhound Manastalker (1) | Felhunter (Ascension: Felhound) | 70 |
| 22220 | Legion War-Hound | Felhunter (Ascension: Felhound) | 70 |
| 18056 | Fiendish Hound (1) | Felhunter (Ascension: Felhound) | 72 |
| 23137 | Fel Gorehound Transform | Felhunter (Ascension: Felhound) | 72 |
| 417 | Felhunter | Felhunter (Ascension: Felhound) | 80 |
| 36301 | Zhaagrym (1) | Felhunter (Ascension: Felhound) | 80 |
| 36302 | Zhaagrym (2) | Felhunter (Ascension: Felhound) | 80 |
| 36303 | Zhaagrym (3) | Felhunter (Ascension: Felhound) | 80 |
| 30491 | Ritssyn | Imp | 1 |
| 416 | Imp | Imp | 5 |
| 5730 | Jezelle's Imp | Imp | 40 |
| 8658 | Hukku's Imp | Imp | 49 |
| 9776 | Flamekin Spitter | Imp | 51 |
| 9708 | Burning Imp | Imp | 54 |
| 9778 | Flamekin Torcher | Imp | 54 |
| 16955 | Chained Trickster | Imp | 54 |
| 16956 | Dust Hopper | Imp | 54 |
| 16957 | Nether Imp | Imp | 54 |
| 18978 | Heckling Fel Sprite | Imp | 57 |
| 14500 | J'eevee | Imp | 58 |
| 14482 | Xorothian Imp | Imp | 59 |
| 18676 | Keb'ezil | Imp | 63 |
| 12922 | Imp Minion | Imp | 66 |
| 22202 | Nightmare Imp | Imp | 70 |
| 24656 | Fizzle | Imp | 70 |
| 24815 | Sunblade Imp | Imp | 70 |
| 25553 | Fizzle (1) | Imp | 70 |
| 25566 | Sunblade Imp (1) | Imp | 70 |
| 30465 | Dan's Test Void Sentry | Imp | 77 |
| 17779 | Outland Imp, Gray | Fel Imp | 1 |
| 17780 | Outland Imp, Orange | Fel Imp | 1 |
| 17781 | Outland Imp, Purple | Fel Imp | 1 |
| 17782 | Outland Imp, Yellow | Fel Imp | 1 |
| 23105 | Fel Imp Minion Transform | Fel Imp | 1 |
| 19136 | Flamewaker Imp | Fel Imp | 58 |
| 17477 | Hellfire Imp | Fel Imp | 61 |
| 19016 | Hellfire Familiar | Fel Imp | 61 |
| 19801 | Illidari Agonizer | Fel Imp | 67 |
| 20887 | Deathforge Imp | Fel Imp | 67 |
| 21021 | Scorch Imp | Fel Imp | 67 |
| 20399 | Terror Imp | Fel Imp | 68 |
| 21135 | Fel Imp | Fel Imp | 68 |
| 22474 | Unstable Fel-Imp | Fel Imp | 68 |
| 22475 | Unstable Fel-Imp Transform | Fel Imp | 68 |
| 18641 | Cabal Familiar | Fel Imp | 69 |
| 18606 | Hellfire Imp (1) | Fel Imp | 70 |
| 20643 | Cabal Familiar (1) | Fel Imp | 70 |
| 21162 | Deathforge Escort | Fel Imp | 70 |
| 21646 | Hellfire Familiar (1) | Fel Imp | 70 |
| 22218 | Insidious Familiar | Fel Imp | 70 |
| 22362 | Deathshadow Imp | Fel Imp | 70 |
| 23404 | Imp Retainer | Fel Imp | 70 |
| 26101 | Fire Fiend | Fel Imp | 70 |
| 17528 | Tzerak | Felguard | 14 |
| 3772 | Lesser Felguard | Felguard | 23 |
| 6115 | Roaming Felguard | Felguard | 28 |
| 4677 | Doomwarder | Felguard | 37 |
| 4680 | Doomwarder Captain | Felguard | 38 |
| 11937 | Demon Portal Guardian | Felguard | 38 |
| 4683 | Doomwarder Lord | Felguard | 39 |
| 18061 | Felguard Netherstorm | Felguard | 50 |
| 6011 | Felguard Sentry | Felguard | 54 |
| 16953 | Forge Camp Patroller | Felguard | 54 |
| 9862 | Jaedenar Legionnaire | Felguard | 55 |
| 19190 | Fel Handler | Felguard | 58 |
| 7735 | Felcular | Felguard | 60 |
| 16954 | Forge Camp Legionnaire | Felguard | 60 |
| 19284 | Invading Felguard | Felguard | 60 |
| 23536 | Nagulon | Felguard | 60 |
| 17000 | Aggonis | Felguard | 63 |
| 16952 | Anger Guard | Felguard | 67 |
| 19802 | Illidari Shocktrooper | Felguard | 68 |
| 19803 | Illidari Destroyer | Felguard | 68 |
| 19822 | Illidari Brute | Felguard | 68 |
| 21519 | Death's Might | Felguard | 68 |
| 22291 | Furnace Guard | Felguard | 70 |
| 23055 | Felguard Degrader | Felguard | 70 |
| 19821 | Illidari Peacekeer | Felguard | 71 |
| 17252 | Felguard | Felguard | 80 |
| 8499 | TEST Uber Succubus | Succubus | 1 |
| 49 | Lesser Succubus | Succubus | 20 |
| 5677 | Summoned Succubus | Succubus | 20 |
| 6270 | Asjorah | Succubus | 20 |
| 30743 | Succubus Transform 01 | Succubus | 20 |
| 18232 | Nimrida | Succubus | 23 |
| 1863 | Succubus | Succubus | 24 |
| 11697 | Mannoroc Lasher | Succubus | 29 |
| 1864 | Greater Succubus | Succubus | 36 |
| 4679 | Nether Maiden | Succubus | 37 |
| 4682 | Nether Sister | Succubus | 38 |
| 4684 | Nether Sorceress | Succubus | 39 |
| 5728 | Jezelle's Succubus | Succubus | 40 |
| 8657 | Hukku's Succubus | Succubus | 49 |
| 9861 | Moora | Succubus | 52 |
| 9860 | Salia | Succubus | 54 |
| 16962 | Griefbringer | Succubus | 54 |
| 9518 | Rakaiah | Succubus | 56 |
| 16960 | Sister of Grief | Succubus | 60 |
| 18730 | Sirigna'no | Succubus | 60 |
| 17399 | Seductress | Succubus | 61 |
| 19290 | Invading Anguisher | Succubus | 61 |
| 19408 | Maiden of Pain | Succubus | 61 |
| 10928 | Succubus Minion | Succubus | 63 |
| 19800 | Illidari Painlasher | Succubus | 68 |
| 19968 | Maiden of Nightmares | Succubus | 68 |
| 21762 | Illidari Tormentor | Succubus | 68 |
| 21776 | Illidari Temptress | Succubus | 69 |
| 18663 | Maiden of Discipline | Succubus | 70 |
| 20655 | Maiden of Discipline (1) | Succubus | 70 |
| 21309 | Painmistress Gabrissa | Succubus | 70 |
| 22219 | Felstorm Motivator | Succubus | 70 |
| 22860 | Illidari Succubus | Succubus | 70 |
| 18614 | Seductress (1) | Succubus | 71 |
| 31529 | Ravishing Betrayer | Succubus | 74 |
| 32394 | Ravishing Betrayer | Succubus | 74 |
| 7129 | Enslaved Voidwalker | Voidwalker | 1 |
| 7130 | Voidwalker Servant | Voidwalker | 1 |
| 7131 | Voidwalker Guardian | Voidwalker | 1 |
| 17887 | Void Critter | Voidwalker | 3 |
| 5676 | Summoned Voidwalker | Voidwalker | 10 |
| 6269 | Azgalaril | Voidwalker | 10 |
| 17550 | Void Anomaly | Voidwalker | 15 |
| 418 | Lesser Voidwalker | Voidwalker | 20 |
| 4627 | Arugal's Voidwalker | Voidwalker | 20 |
| 1860 | Voidwalker | Voidwalker | 24 |
| 1861 | Greater Voidwalker | Voidwalker | 26 |
| 24476 | Minor Voidwalker | Voidwalker | 35 |
| 5729 | Jezelle's Voidwalker | Voidwalker | 40 |
| 8996 | Voidwalker Minion | Voidwalker | 42 |
| 8656 | Hukku's Voidwalker | Voidwalker | 49 |
| 16974 | Rogue Voidwalker | Voidwalker | 60 |
| 16975 | Uncontrolled Voidwalker | Voidwalker | 60 |
| 19233 | Flying Voidwalker | Voidwalker | 60 |
| 19287 | Invading Voidwalker | Voidwalker | 60 |
| 20145 | Unstable Voidwalker | Voidwalker | 60 |
| 17014 | Collapsing Voidwalker | Voidwalker | 61 |
| 19599 | Void Servant | Voidwalker | 63 |
| 17981 | Voidspawn | Voidwalker | 65 |
| 18868 | Voidfiend | Voidwalker | 68 |
| 19356 | Void Wanderer | Voidwalker | 68 |
| 20664 | Void Traveler (1) | Voidwalker | 70 |
| 32260 | Enslaved Minion | Voidwalker | 78 |
| 32316 | Dark Messenger | Voidwalker | 78 |
