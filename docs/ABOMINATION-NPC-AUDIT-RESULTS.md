# Abomination NPC spell audit — 2026-09-22

Status: live export reviewed; no server changes. Export completed without missing reads and all recorded file hashes verified. Evidence is configuration/source review, not an in-game combat test.

## Findings

- Native Abomination Hook **59395** explicitly triggers **Hooked 59832** through its third effect (effect 140). Treacherous Guardian **31532** has a SmartAI cast of 59395 on aggro. This is a concrete native reference for applying the 60-second anti-repeat aura.
- Ascension Constricting Chain **80188** has a target exclusion for 59832 but no trigger to apply it. The native hook supports the proposed design; it does not prove how the Ascension server implemented that pet spell.
- Meathook casts **52696 Constricting Chains**. Its native effects are periodic damage and stun; this is not the imported pet spell's 100% weapon damage and three-second root. **58823** is another native Constricting Chains definition with the same effect types.
- Direct SmartAI casts include native Strike **18368** and several Cleaves, including **15496, 40504, 53633, 27794 and 70191**. Different IDs have different tuning; they are not drop-in equivalents for imported 80186/80190.
- **50335 Scourge Hook** is used by multiple Abominations. A hook/pull spell should not be substituted for the pet root without an explicit behavior decision.

## Pet implementation implications

Retain the approved Ascension Strike/Cleave definitions and their energy/cooldown values. Implement Constricting Chain's Hooked application explicitly if it is included in a later wave; test hit, immunity and repeat-target behavior. Do not copy native hook movement or boss mechanics into the pet spell. The current two-spell Abomination test package still withholds Constricting Chain.

## Direct SmartAI cast inventory

These are direct creature SmartAI cast actions. Template spell slots, addon auras and compiled boss scripts are separate evidence; presence in a slot alone does not prove a spell is cast. Shared timed action lists were exported but are not included as direct creature casts in this table.

| Spell | Name | Creature entries |
|---|---|---|
| 3106 | Aura of Rot | 412 |
| 3148 | Head Crack | 16247 |
| 3396 | Corrosive Poison | 16246 |
| 5568 | Trample | 10439, 14697 |
| 6253 | Backhand | 29769, 29860 |
| 7160 | Execute | 16017 |
| 8014 | Tetanus | 16246 |
| 8269 | Frenzy | 14682 |
| 8601 | Slowing Poison | 10417 |
| 10101 | Knock Away | 1805, 1850, 10414 |
| 11020 | Petrify | 8120 |
| 11428 | Knockdown | 8544 |
| 12627 | Disease Cloud | 8567 |
| 12795 | Frenzy | 8567 |
| 12946 | Putrid Stench | 1850 |
| 13444 | Sunder Armor | 16245 |
| 13445 | Rend | 16247 |
| 14099 | Mighty Blow | 8543 |
| 15088 | Flurry | 10439 |
| 15496 | Cleave | 30689, 31098 |
| 16345 | Disease Cloud | 10414 |
| 16508 | Intimidating Roar | 14682 |
| 16577 | Disease Cloud | 8545 |
| 16790 | Knockdown | 14697 |
| 16809 | Spawn Bile Slime | 10416 |
| 16865 | Spawn Bile Slimes | 10416 |
| 16866 | Venom Spit | 10417 |
| 17307 | Knockout | 10439 |
| 17650 | Altered Cauldron Toxin | 1850 |
| 17745 | Diseased Spit | 14682 |
| 18328 | Incapacitating Shout | 12263 |
| 18368 | Strike | 15195 |
| 19128 | Knockdown | 15195 |
| 25007 | Wickerman Guardian Ember | 15195 |
| 27758 | War Stomp | 16017 |
| 27794 | Cleave | 16017 |
| 27807 | Bile Vomit | 16018 |
| 27891 | Acidic Sludge | 16029 |
| 28032 | Zap Crystal | 14697 |
| 28131 | Frenzy | 31099 |
| 28265 | Scourge Strike | 14697 |
| 28313 | Aura of Fear | 14697 |
| 28362 | Disease Cloud | 16029 |
| 29266 | Permanent Feign Death | 29769 |
| 31389 | Knock Away | 16245 |
| 35426 | Arcane Explosion Visual | 29769 |
| 37548 | Taunt | 29860 |
| 40504 | Cleave | 16245, 25383, 26624, 29719, 30920, 31140, 33704, 37022 |
| 48697 | Mighty Blow | 26555 |
| 49703 | Bile Vomit | 26624 |
| 50335 | Scourge Hook | 25383, 27797, 27808, 29115, 29186, 29719, 30689, 30696, 31098, 31140 |
| 50366 | Plague Cloud | 25684 |
| 51356 | Vile Vomit | 27808 |
| 52523 | Explode Abomination:Bloody Meat | 31692 |
| 52525 | Disease Cloud | 27736 |
| 52527 | Wretching Bile | 28201 |
| 53633 | Cleave | 29115, 29186 |
| 54326 | Bile Vomit | 16018 |
| 54331 | Acidic Sludge | 16029 |
| 56426 | Execute | 16017 |
| 56427 | War Stomp | 16017 |
| 56646 | Enrage | 29769, 29860 |
| 58412 | Hateful Strike | 31099 |
| 58808 | Disease Cloud | 27736 |
| 58810 | Wretching Bile | 28201 |
| 58995 | Exploding Corpse | 31140 |
| 59018 | Bile Vomit | 26624 |
| 59228 | Volatile Infection | 26555 |
| 59395 | Abomination Hook | 31532 |
| 59580 | Burst at the Seams | 31692 |
| 70191 | Cleave | 37546 |
| 70371 | Enrage | 37546 |
| 71140 | Scourge Hook | 37022 |
| 71150 | Plague Cloud | 37022 |

## Compiled-script coverage

The export includes matching source for: `boss_kelthuzad_minion`, `boss_meathook`, `boss_patchwerk`, `npc_gluttonous_abomination`, `npc_heated_battle`, `npc_hor_lumbering_abomination`, `npc_hyjal_ground_trash`, `npc_pallid_horror`, `npc_putricide_mutated_abomination`, `npc_wg_quest_giver`. Entire multi-creature source files were retained locally, so unrelated spells in those files must not be attributed to an Abomination without following its specific AI class.

No full extracted source or DBC archive is published in the repository. The local export is `Hero_Abomination_Test/npc-audit-3`.
