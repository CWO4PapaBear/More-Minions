# Primary companion stable UI compatibility

Roguetest's fresh PTR export shows a living level-75 Abomination saved as PetType=1, slot=0, CreatedBySpell=885, with zero purchased stable slots. The stable menu opens. Existing server gossip and load handlers already integrate More Minions authorization and creature-family checks.

The native stable UI calls HasPetUI and clears the pet display and purchase controls if its hunter-pet result is false. A scoped Lua 5.1 environment for PetStable_Update and PetStable_OnEvent treats a matching server-listed current primary pet as stable-compatible when an imported capture ability is known. It supplies safe icon/family display fallbacks for listed pets. Global HasPetUI and GetStablePetInfo are unchanged; storage, retrieval, prices and slot limits remain native/server-authoritative.

Covers Dominate Undead (899), Tame Dragonkin (896), Tether Elemental (93558), and Enslave Demon (93569). This does not activate unsupported families or enable storage of secondary guardians. Ordinary Classic clients without the imported capture spells retain their existing UI behavior. The display adapter is not an authorization mechanism; the server may still reject a pet it does not consider storable.

Test-Client.py reproduces the blank panel using the local reference PetStable.lua, then exercises all four groups, purchase-control visibility, ordinary pet exclusion and unchanged global APIs. This is a mocked API test, not proof of live-server stable transactions. Pass a locally supplied PetStable.lua path as its argument; extracted reference files are not distributed.

Close WoW and run Install-Client.py --wow-closed in WSL. The installer hashes and backs up the existing addon TOC, then adds only StableCompatibility.lua. No server restart, SQL or MPQ changes. Launcher publication is pending this in-game check.

## Test in game

Reopen the stable with Abomination active. Confirm its icon and purchase price appear, buy one normal slot, store and retrieve it, then relog and repeat. Verify name, level and four skills persist. Repeat with captured Demons and supported Elementals/Dragonkin when available; no assertion is made that unfinished families are enabled. Secondary Demon Mastery/Beckoned guardians must not occupy stable slots.

## Patch notes

Restore stable pet display and slot-purchase controls for imported primary companions on non-Hunter characters. Uses the standard shared stable; secondary guardians remain separate. In-game acceptance pending.
