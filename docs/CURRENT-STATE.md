# Current state and decisions

Recorded September 17, 2026 from HeroFreePick 0.39.9. No More Minions server implementation exists.

## Interface implemented in HeroFreePick

- Five bundle purchases stage their 26 linked skills together, with no per-child purchase. Removing the parent removes its local grants; cancel restores the prior plan.
- Only the group-controlling ability has a Shift-expanded list. A same-named child such as Tame Beast does not open another group list.
- Members sort by required level; icon rows put the icon left and the name right. Child icons retain their individual artwork; small parent badges open the parent tooltip.
- Learned-list grouping places the parent first, with smaller indented children where the parent is visible. Passive parents are hidden by the existing passive filter.
- Imported descriptions are shown without an A52 attribution prefix. Unevaluated spell formulas remain placeholders instead of invented values.
- Classic excludes custom packages. Class+ follows its original class; Hybrid follows its two classes; Hero can preview all packages within the configured budgets.
- Demon Mastery costs 2 AP and 2 Epic gems, starts at level 1 and includes Summon Imp. Its other summons follow recorded member levels and automatic local level grants.

## Not implemented or demonstrated

No authoritative purchase, grant/refund transaction, companion taming, permanent ownership, new creature eligibility, cross-class pet lifecycle, pet AI/scaling, stable support or server save/load has been implemented by this work. Tests are Lua UI mocks and data checks, not proof of real pet behavior. No separate More Minions addon exists yet.

## Recorded design decisions

- Companion bundles retain 4 AP / 2 Epic gems in FreePick; they do not inherit the 2 AP Mastery rule.
- Buying multiple groups does not grant multiple simultaneous pets.
- Keep Beast taming and ordinary demon summons distinct from permanent taming of Demons, Undead, Dragonkin and Elementals.
- Dragonkin Lore and Dismiss Dragonkin artwork were swapped at the user's request; preserve the effective mappings in the catalog.
- Wild Imps remain research, because no equivalent bundle was identified in reviewed records.
- Source class assignments are UI classifications, not proof of native server support for those classes.
- Standalone access may deliberately enable early companions, but must not silently change Classic defaults in HeroFreePick.

## Work chronology

0.32.0: first four bundle previews. 0.32.2: missing companion textures packaged in FreePick. 0.33.0: Elemental package and descriptions, Wild Imp review. Subsequent UI work added grouping, retained child icons, automatic mastery grants and Classic separation. This repository captures the resulting state without copying unrelated FreePick features.
