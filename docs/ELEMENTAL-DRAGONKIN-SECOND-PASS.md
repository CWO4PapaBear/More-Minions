# Elemental and Dragonkin reference second pass — 2026-09-22

Status: reference review only. No new Elemental/Dragonkin mappings, definitions or handlers installed.

Six available SkillLineAbility tables were compared: Area 52 patch-D, shared patch-M and four enUS versions. Shared patch-M agrees with Area 52 for these family links; enUS tables add no links for these custom family skill lines. The extracted COA and classless-wildcard source and Season 9 addon were searched for representative pet spell IDs and `scalingbp`; no matching handler implementation was found in those searched files. This is not a claim that every archive contains no other implementation.

| Category | Listed families | Families with linked skills | Distinct linked spells | No linked skills |
|---|---:|---:|---:|---:|
| Elemental | 88 | 46 | 133 | 42 |
| Dragonkin | 143 | 47 | 151 | 96 |

## Recoverable scaling evidence

SpellDescriptionVariables row 182 supplies this tooltip expression:

```text
$scalingbp=${(0.0267291844060354+0.0048541098014737*$PL+0.0001859597762293*$PL*$PL)}
```

This is a concrete client formula, not proof that a stock server will evaluate it. A server handler must explicitly apply the agreed level scaling to direct damage, periodic damage and healing. Owner versus pet level, additional spell-power scaling and scaling applied by shared passives must be reconciled to avoid applying the same multiplier twice.

Examples include Wind Shock (892101), Boulder (892111), Water Bolt (892131), Lesser Fireball (91755) and Chain Lightning (91829). Fire Blast (892121) has malformed source tooltip punctuation around its formula and needs normalized display text.

The shared category tables also contain 15 Elemental and 14 Dragonkin passive/scaling records: avoidance, invigoration, scaling and tamed-pet passives. Elementals additionally reference damage modifier 1132234. These are dependencies requiring effect review, not ordinary pet-bar buttons.

## Implementation order

1. Implement and verify the recovered level-scaling rule for basic bolts, damage-over-time and healing.
2. Resolve triggered spells, shared scaling passives, target selection and autocast behavior.
3. Review creature-to-family assignments separately; client family links do not identify every server creature template.
4. Enable reviewed families after definition, client-asset and combat checks; keep unsupported families unavailable.

## Linked family skills

The table records reference links, not a claim that the skills are deployed. Empty review reasons in the machine-readable companion report mean the earlier candidate filter did not flag that spell; they do not establish runtime correctness.

| Category | Family | Linked skills |
|---|---|---|
| Elemental | 301 Air Elemental | 892101 Wind Shock (Pet), 892102 Lightning Bolt (Pet), 892103 Wind Shear |
| Elemental | 302 Earth Elemental | 892111 Boulder, 892112 Earthshatter, 892113 Rockbiter Strike |
| Elemental | 303 Fire Elemental | 892121 Fire Blast (Pet), 892122 Fire Wall, 892123 Blazing Speed |
| Elemental | 304 Water Elemental | 892131 Water Bolt (Pet), 892132 Water Spout (Pet), 892133 Rejuvenating Water (Pet) |
| Elemental | 305 Magma Elemental | 892141 Stomp, 892142 Molten Blast, 892143 Magma Splash |
| Elemental | 306 Ice Elemental | 892151 Avalanche, 892152 Frost Nova (Pet), 892153 Blizzard (Pet) |
| Elemental | 308 Mana Elemental | 892161 Mana Burn (Pet), 892162 Slow, 892163 Replenish Mana |
| Elemental | 309 Entropic Elemental | 892171 Entropic Shock, 892172 Entropic Streak, 892173 Entropic Shield |
| Elemental | 310 Mojo Elemental | 892181 Dark Jujubolt, 892182 Mojo Wave, 892183 Mojo Beam |
| Elemental | 311 Shadow Elemental | 892191 Shadow Mark, 892192 Shadow Shock, 892193 Enveloping Shadows |
| Elemental | 323 Steam Elemental | 892201 Water Mark, 892202 Steam Blast, 892203 Steam Push |
| Elemental | 324 Arcane Elemental | 892211 Arcane Bolt, 892212 Drain Power, 892213 Blink |
| Elemental | 326 Air Revenant | 892221 Air Whirl, 892222 Air Enchantment, 892223 Lightning Blink |
| Elemental | 327 Earth Revenant | 892231 Earth Strike, 892232 Earth Enchantment, 892233 Stomp |
| Elemental | 328 Fire Revenant | 892241 Flame Strike, 892242 Fire Enchantment, 892243 Growing Embers |
| Elemental | 329 Water Revenant | 892251 Water Splash, 892252 Water Enchantment, 892253 Water Wave |
| Elemental | 331 Death Revenant | 892261 Shadow Cleave, 892262 Death Enchantment, 892263 Death Coil |
| Elemental | 332 Ice Revenant | 892271 Ice Slash, 892272 Ice Enchantment, 892273 Ice Barrier |
| Elemental | 350 Phoenix | 892281 Smoldering Feathers, 892282 Fire Swoop, 892283 Phoenix Egg |
| Elemental | 356 Lasher | 92498 Thrash, 92499 Razor-sharp Barbs, 892297 Virulent Poison |
| Elemental | 358 Constrictor Orchid | 92498 Thrash, 92504 Nature's Bounty, 892297 Virulent Poison |
| Elemental | 359 Constrictor Lasher | 92498 Thrash, 92506 Thorn Volley, 892297 Virulent Poison |
| Elemental | 360 Mutated Orchid | 92498 Thrash, 92512 Tranqulizing Dust, 892297 Virulent Poison |
| Elemental | 363 Bloodpetal Lasher | 92498 Thrash, 92508 Bloodthirsty, 892297 Virulent Poison |
| Elemental | 364 Frostpetal Orchid | 92498 Thrash, 92500 Frost Barrier, 892297 Virulent Poison |
| Elemental | 365 Frostpetal Lasher | 92498 Thrash, 92507 Icicle, 892297 Virulent Poison |
| Elemental | 367 Deathpetal Lasher | 92498 Thrash, 92510 Summon Deathpetal Effigy, 892297 Virulent Poison |
| Elemental | 368 Stone War Golem | 92502 Thunderclap, 92503 Taunt, 92516 Stoneform |
| Elemental | 369 Stone Siege Golem | 92519 Throw Boulder, 92522 Cannon Shot, 92523 Cannon Blast |
| Elemental | 370 Dark Iron War Golem | 92502 Thunderclap, 92503 Taunt, 92524 Oil Spill |
| Elemental | 372 Ragereaver War Golem | 92502 Thunderclap, 92503 Taunt, 92515 Enrage |
| Elemental | 373 Ragereaver Siege Golem | 92515 Enrage, 92522 Cannon Shot, 92523 Cannon Blast |
| Elemental | 374 Molten War Golem | 92502 Thunderclap, 92503 Taunt, 92518 Immolation |
| Elemental | 375 Molten Siege Golem | 92520 Hurl Flaming Boulder, 92522 Cannon Shot, 92523 Cannon Blast |
| Elemental | 376 Iron War Golem | 92502 Thunderclap, 92503 Taunt, 92524 Oil Spill |
| Elemental | 377 Iron Siege Golem | 92502 Thunderclap, 92503 Taunt, 92524 Oil Spill |
| Elemental | 378 Drakkari War Golem | 92502 Thunderclap, 92503 Taunt, 92524 Oil Spill |
| Elemental | 379 Drakkari Siege Golem | 92502 Thunderclap, 92503 Taunt, 92524 Oil Spill |
| Elemental | 380 Runic War Golem | 92502 Thunderclap, 92503 Taunt, 92524 Oil Spill |
| Elemental | 381 Runic Siege Golem | 92502 Thunderclap, 92503 Taunt, 92524 Oil Spill |
| Elemental | 382 Verdant Bog Beast | 92526 Infected Wound, 92527 Tendon Rip, 92528 Moss Covered Hands |
| Elemental | 383 Fungal Bog Beast | 92530 Fungal Regrowth, 92531 War Stomp, 92533 Wild Growth |
| Elemental | 384 Hardwood Treant | 93532 Treant Tamed Pet Passive 12 (DND), 93533 Treant Avoidance, 93536 Treant Invigoration, 93540 Treant Tamed Pet Passive 07 (DND), 93541 Treant Tamed Pet Passive 06 (DND), 93542 Treant Tamed Pet Passive 05 (DND), 93543 Treant Tamed Pet Passive 04 (DND), 93544 Treant Tamed Pet Passive 03 (DND), 93545 Treant Tamed Pet Passive 02 (DND), 93546 Treant Tamed Pet Passive 01 (DND), 93547 Treant Tamed Pet Passive 00 (DND), 93548 Treant Tamed Pet Passive 10 (DND), 93549 Treant Tamed Pet Passive 09 (DND), 93715 Entangling Roots, 93716 Thorns, 93717 Rejuvenation |
| Elemental | 385 Dreadwood Treant | 93584 Treant Tamed Pet Passive 12 (DND), 93585 Treant Avoidance, 93588 Treant Invigoration, 93592 Treant Tamed Pet Passive 07 (DND), 93593 Treant Tamed Pet Passive 06 (DND), 93594 Treant Tamed Pet Passive 05 (DND), 93595 Treant Tamed Pet Passive 04 (DND), 93596 Treant Tamed Pet Passive 03 (DND), 93597 Treant Tamed Pet Passive 02 (DND), 93598 Treant Tamed Pet Passive 01 (DND), 93599 Treant Tamed Pet Passive 00 (DND), 93600 Treant Tamed Pet Passive 10 (DND), 93601 Treant Tamed Pet Passive 09 (DND), 93718 Petrified Bark, 93720 Corruption, 93721 Mana Burn |
| Elemental | 386 Winterwood Treant | 93663 Treant Tamed Pet Passive 12 (DND), 93664 Treant Avoidance, 93667 Treant Invigoration, 93671 Treant Tamed Pet Passive 07 (DND), 93672 Treant Tamed Pet Passive 06 (DND), 93673 Treant Tamed Pet Passive 05 (DND), 93674 Treant Tamed Pet Passive 04 (DND), 93675 Treant Tamed Pet Passive 03 (DND), 93676 Treant Tamed Pet Passive 02 (DND), 93677 Treant Tamed Pet Passive 01 (DND), 93678 Treant Tamed Pet Passive 00 (DND), 93679 Treant Tamed Pet Passive 10 (DND), 93680 Treant Tamed Pet Passive 09 (DND), 93722 Frost Shock, 93723 Ice Lash, 93724 Replenishment |
| Elemental | 387 Softwood Treant | 93725 Holy Shock, 93726 Renew |
| Dragonkin | 402 Black Whelp | 91755 Lesser Fireball, 91757 Fireball (Pet), 91758 Fire Blast (Pet) |
| Dragonkin | 403 Black Drake | 91834 Blast Wave (Pet), 91835 Dark Breath, 91836 Swipe |
| Dragonkin | 404 Black Dragon | 891010 Brood Power: Black, 891012 Dark Breath, 891013 Tail Sweep, 891014 Shadow Cleave |
| Dragonkin | 406 Black Drakonid | 91860 Brood Power: Black, 91861 Shadow Nova, 91862 Shockwave (Pet) |
| Dragonkin | 407 Black Scalebane | 91888 Thunderclap, 91889 Fiery Cleave, 91890 Strike |
| Dragonkin | 408 Black Wyrmkin | 91905 Dark Bolt, 91906 Rain of Fire (Pet), 91907 Shadow Nova |
| Dragonkin | 414 Blue Whelp | 91759 Arcane Bolt, 91761 Frostbolt (Pet), 91762 Drain Mana |
| Dragonkin | 415 Blue Drake | 91840 Devour Magic, 91842 Ice Beam, 91843 Frost Breath, 891893 Frost Strike |
| Dragonkin | 416 Blue Dragon | 891020 Brood Power: Blue, 891021 Frost Breath, 891022 Drain Mana, 891023 Ice Beam |
| Dragonkin | 418 Blue Drakonid | 91863 Brood Power: Blue, 91864 Thunderclap (Pet), 91865 Shockwave (Pet) |
| Dragonkin | 419 Blue Scalebane | 91892 Frostbite Weapon, 91893 Frost Strike, 91894 Frost Nova |
| Dragonkin | 420 Blue Wyrmkin | 91909 Cone of Cold (Pet), 91911 Deep Freeze (Pet), 91912 Arcane Barrage (Pet) |
| Dragonkin | 426 Bronze Whelp | 91765 Sand Bomb, 91766 Chrono Mend, 91767 Timelink |
| Dragonkin | 427 Bronze Drake | 91844 Sand Breath, 91845 Timelink, 91846 Time Shock |
| Dragonkin | 428 Bronze Dragon | 891030 Brood Power: Bronze, 891033 War Stomp, 891034 Sand Breath, 891035 Swipe |
| Dragonkin | 430 Bronze Drakonid | 91866 Brood Power: Bronze, 91868 Arcane Bomb, 91869 Shockwave |
| Dragonkin | 431 Bronze Scalebane | 91895 Time Cleave, 91896 Time Stop, 92045 Transcendental Scales |
| Dragonkin | 438 Green Whelp | 91821 Acid Spit, 91822 Minor Rejuvenation, 91823 Sleep |
| Dragonkin | 439 Green Drake | 91847 Corrosive Acid Breath, 91848 Nature's Wrath, 91849 Nature's Bloom |
| Dragonkin | 440 Green Dragon | 891040 Brood Power: Green, 891042 Nature's Bloom, 891043 Tail Sweep, 891044 Corrosive Acid Breath |
| Dragonkin | 442 Green Drakonid | 91873 Brood Power: Green, 91874 Thunderclap, 91875 Shockwave |
| Dragonkin | 443 Green Scalebane | 91897 Thorns Aura, 91898 Acid Splash, 91899 Pummel (Pet) |
| Dragonkin | 444 Green Wyrmkin | 91914 Wrath (Pet), 91915 Nature's Wrath, 91916 Restore Nature |
| Dragonkin | 450 Red Whelp | 91768 Fireball (Pet), 91819 Fire Blast (Pet), 91820 Fire Shield (Pet) |
| Dragonkin | 451 Red Drake | 91850 Flame Breath, 91851 Wing Buffet, 91852 Swipe |
| Dragonkin | 452 Red Dragon | 891050 Brood Power: Red, 891051 Flame Breath, 891052 Bellowing Roar, 891053 Fiery Cleave |
| Dragonkin | 454 Red Drakonid | 91879 Brood Power: Red, 91880 War Stomp, 91881 Burning Fury |
| Dragonkin | 455 Red Scalebane | 91885 Fiery Cleave, 91886 Fire Nova (Pet), 91887 Strike |
| Dragonkin | 462 Chromatic Whelp | 91945 Chromatic Bolt, 91946 Chromatic Blast, 91947 Chromatic Shield |
| Dragonkin | 463 Chromatic Drake | 91853 Wing Buffet, 91948 Chromatic Swipe, 91949 Chromatic Breath |
| Dragonkin | 466 Chromatic Drakonid | 91950 Brood Power: Chromatic, 91951 Chromatic Shockwave, 91952 Chromatic Flurry |
| Dragonkin | 467 Chromatic Scalebane | 91901 Disarm, 91953 Chromatic Strike, 91959 Reinforcement |
| Dragonkin | 470 Chromatic Drakeadon | 91923 Enrage, 91954 Brood Power: Chromatic, 91955 Chromatic Breath |
| Dragonkin | 474 Infinite Whelp | 91832 Shadow Bolt (Pet), 91833 Impending Death, 92067 Timebreak |
| Dragonkin | 475 Infinite Drake | 91857 Swipe, 91858 Timerend, 91859 Shadow Breath |
| Dragonkin | 476 Infinite Dragon | 891060 Shadow Breath, 891061 Shadowstep, 891062 Timerend, 891063 Shadow Nova |
| Dragonkin | 478 Infinite Drakonid | 91882 Shadowstep, 91883 Shockwave (Pet), 91884 Shadow Nova |
| Dragonkin | 479 Infinite Scalebane | 91902 Shadow Cleave, 91903 Shadowguard, 91904 Void Strike |
| Dragonkin | 480 Infinite Wyrmkin | 91918 Shadow Blast, 91919 Shadow Spiral, 91922 Veil of Shadow |
| Dragonkin | 486 Twilight Whelp | 91825 Twilight Bolt, 91826 Binding Twilight, 91827 Twilight Blast |
| Dragonkin | 488 Twilight Dragon | 891070 Bellowing Roar, 891071 Twilight Breath, 891072 Twilight Blast, 891073 Twilight Cleave |
| Dragonkin | 491 Twilight Scalebane | 91900 Twilight Cleave, 891100 Silent Twilight, 891101 Twilight Nova |
| Dragonkin | 499 Netherwing Drake | 91854 Nether Blast, 91855 Arcane Blast, 91856 Intangible Presence, 891895 Strike |
| Dragonkin | 500 Netherwing Dragon | 891080 Nether Breath, 891081 Nether Spike, 891082 Arcane Blast, 891083 Nether Sweep |
| Dragonkin | 502 Netherwing Drakonid | 91876 Sunder Armor, 91877 Shockwave (Pet), 91878 Nether Spike, 91890 Strike |
| Dragonkin | 510 Plagued Whelp | 91828 Poison Bolt, 91956 Plague Cloud, 91957 Plague Blast |
| Dragonkin | 541 Faerie Dragon | 91829 Chain Lightning (Pet), 91830 Mana Burn, 91831 Blink (Pet) |

## Source verification

Exact source filenames, SHA-256 hashes, alternate-table results, family links and withheld reasons are recorded in [the audit JSON](../data/family-reconciliation/elemental-dragonkin-second-pass.json). Original reference definitions remain in `docs/pet-family-review/pet-family-reference.json`.
