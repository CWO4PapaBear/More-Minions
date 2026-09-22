# Neutral capture and family reconciliation - 2026-09-22

Status: staged source changes and reviewed candidates; not built or activated by this work. The neutral-only build can proceed independently. No SQL or client patch has been applied.

## Capture rule
All four imported capture groups (Demon, Undead, Elemental, Dragonkin) permit neutral attackable targets. Friendly targets remain excluded. Ownership, level, rank, NPC/script/vehicle protection, range, line of sight, pet-slot checks, channel attention and haste handling remain unchanged. Stock Classic capture spells are unchanged.

## Live audit
The read-only export has no missing reads. There are 5,274 creature templates in the four categories and 701 currently enabled family mappings. Ascension lists 312 family names; 131 have linked ability sets, and 93 of those have supported skill candidates. These counts do not imply all those families exist in WotLK or are ready to enable.

Expanded model and texture classification is staged. Dragon flight classification uses model plus texture, not the shared model alone. Ambiguous multi-model templates remain withheld. Model-derived classifications are local decisions, not recovered Ascension server assignments.

## Approved stock fallback
Use matching stock WotLK pet skills when Ascension has no usable family set. First fallback profiles: Imp, Fel Imp, Felhound, Felstalker, Succubus, Voidwalker and Felguard, totaling 106 stock spell ranks. The current model review identifies 174 new unprotected creature mapping candidates across six of these families; Felstalker-specific classification remains unresolved. Preserve native skill unlock levels. Select the highest eligible rank per spell chain for learned skills and Lore. Do not automatically grant Warlock scaling, Demonic Pact or Empowered Imp to enslaved pets.

## Still required
- Compile and review the neutral-only server build before maintenance activation.
- Verify the stock-family build against current minion source and pet-specific spell bindings; apply new mappings with rollback protection only after that validation.
- Resolve ambiguous species/subfamily assignments, especially shared humanoid models and Felhound/Felstalker variants.
- Implement or supply definitions/assets for additional Ascension-only skill sets before enabling their families. Unsupported families remain unavailable, as previously requested.
- Test neutral creatures, friendly/protected rejections, channel haste, death/interruption, stable persistence, skill rank updates and family-specific talents in game.

The files in tools/staged-neutral-families are guarded patch inputs for the existing integrated More Minions server source. They are not a standalone installer. Full module source reconciliation is a separate pending publishing task; this commit does not imply the older repository foundation now contains the entire live server implementation.
