# Family icons for the classic stable

Use the catalog's actual family icons, including the Abomination stitched head (family 203), rather than one creature-type icon for all Undead, Demons, Elementals or Dragonkin. Layout and verified stable transactions remain unchanged.

The local package resolves 345 family icon references into 88 shared image assets and 2,673 creature-to-family display mappings. The Observer catalog path typo is corrected to the existing warlock_summon_beholder asset. Mappings are display-only and do not enable any withheld capture family. Imported assignments use the reviewed creature catalog plus the approved Abomination mapping overrides.

Beasts use their family icon from the native client or family name and cache it by creature entry for storage. The same icon is used in both boxes. An unknown entry without family evidence gets a question mark rather than an invented family assignment. Stored Beasts never previously seen and unavailable through the native API still require retrieving once to populate that cache.

Validation: all assets decode, all catalog references resolve, Abomination 16247 maps to family 203, Lua 5.1 classic controls/actions and Beast current/stored cache tests pass, and isolated installer/idempotency/drift checks pass. In-game icon verification is pending.

Close WoW and run the local Install-Client.py with --wow-closed. No server restart, SQL or MPQ changes. Launcher publication remains pending.

PTR owner confirmation (September 23, 2026): Undead and Demon stabling both work. Classic interface appearance was also confirmed. This does not establish Elemental/Dragonkin behavior, relog persistence or explicit confirmation of each family icon.

Source control contains the addon logic, tests, installer and manifest only. Extracted artwork is excluded from the source repository; the complete pinned local installation package contains the required assets. A fresh source checkout alone is not an installable client release.
