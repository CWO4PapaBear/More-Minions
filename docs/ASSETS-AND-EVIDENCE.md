# Assets and evidence

The reviewed sources were local extracted Area 52 Spell.dbc, CharacterAdvancement.dbc, CharacterAdvancementData.json, SpellIcon.dbc and texture archives. The existing FreePick workspace retains the detailed review JSON. This repository records selected IDs, costs and effective icon references, not proprietary server code or a complete client data export.

The catalog is extracted from the evaluated HeroFreePick definitions, including later icon overrides. Source file hashes are in data/provenance.json. Display paths beginning Interface/AddOns/HeroFreePick are references to assets in that addon; those files are not shipped here and are not a standalone dependency contract.

The earlier audit found missing custom textures for several Demon/Undead/Dragonkin abilities. FreePick later bundled replacements from the reviewed client and added Elemental Lore artwork. Dragonkin Lore/Dismiss were subsequently swapped by design. Some earlier audit documents describe the pre-import state; the effective catalog mappings are the current interface reference.

No texture binaries, DBCs, MPQs, executables, credentials, SavedVariables or personal layout presets are included. Asset availability does not establish redistribution permission. Review rights or choose stock/replacement artwork before a standalone release. A software license has not been chosen for More Minions yet; repository visibility alone does not grant a license.

Wild Imp findings are limited to reviewed client records: temporary Hand of Gul'dan summons and vanity appearance data were found, not a permanent tame/recall bundle. Creature allowlists, authoritative stats and live server behavior were not available in that review.
