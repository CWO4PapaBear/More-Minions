# Pet mappings - all four categories

Snapshot: 2026-09-22 read-only PTR export plus the verified Valley of Trials supplement. **No new family mappings or creature-template changes have been installed.** Neutral attackable capture eligibility is already active.

- **Active:** database mapping was enabled in the export. This does not guarantee capture: level, friendliness, ownership, protection and channel checks still apply.
- **Staged:** a proposed assignment exists; server profile/build/effect validation or installation remains pending.
- **Blocked:** assignment is ambiguous, skills/definitions are missing, or template protections exclude capture. Some templates have multiple reasons. Missing spell IDs are not the only possible implementation gaps.

These are creature **templates**, including unspawned/test templates, not a list of guaranteed world encounters. Counts are not spawn counts. Staged model/texture classifications are local proposals, not recovered Ascension server mappings.

| Category | Active | Staged | Blocked | Detailed review |
| --- | ---: | ---: | ---: | --- |
| Demons | 242 | 178 | 543 | [Demons](pet-mappings/demons.md) |
| Undead | 436 | 12 | 2079 | [Undead](pet-mappings/undead.md) |
| Elementals | 13 | 0 | 987 | [Elementals](pet-mappings/elementals.md) |
| Dragonkin | 10 | 0 | 775 | [Dragonkin](pet-mappings/dragonkin.md) |

## Valley of Trials overrides

- **Felstalker (3102): Felhunter family**, preserving levels 3-4. Reference family 110 is named Felhound in Ascension; this is not family 111 merely because the creature is named Felstalker. The live export has no mapping. There are 16 spawns in map 1.
- **Vile Familiar (3101): Demon type, Imp family, levels 1-4.** Verified live baseline: Humanoid, no family, levels 3-4, 37 spawns in map 1. This is a requested template-wide override; it affects all spawns using entry 3101. Its SmartAI, loot, faction and spawn locations are to be preserved.

[All family skill-readiness entries](pet-mappings/families.md) · [Downloadable creature review CSV](pet-mappings/creatures.csv)

A family without a suitable Ascension skill set may use matching stock WotLK pet skills under the owner's approved policy. Families without either remain unavailable. The stock fallback set and rank-selection code are staged, not activated.
