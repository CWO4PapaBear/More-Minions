# More Minions stable bridge — PTR candidate

The client reported no native stable rows for a saved Abomination. Display-only compatibility restored the model and purchase prompt, but native slot clicks still could not store it. This candidate adds a server-authenticated list and explicit Store current, Retrieve / swap, and Buy slot buttons inside the stable frame.

The server calls existing stable handlers. Their ownership, family eligibility, living-pet, purchased-slot, money and persistence rules remain authoritative. The bridge additionally checks capture access, stable-master proximity, alive/out-of-combat state and rejects mounted or flying requests. Only primary HUNTER_PET records appear; independent summoned guardians do not enter the stable.

All four imported capture categories use the same bridge: Demon, Undead, Elemental and Dragonkin. This does not enable withheld families. A mixed collection may also contain ordinary Beasts. Only the current Beast shows happiness; non-Beasts and stored pets do not reuse a live pet's happiness tooltip. Characters without an imported capture ability retain the native interface.

## Status

Passed: Lua 5.1 transport/display tests, C++ command-contract tests with mocked native handlers, and isolated installer/idempotency/drift checks. The full PTR compile and in-game store/retrieve validation are still pending. No activation or launcher publication is performed by preparing this package. The previous Beast-only happiness/portrait client repair is a prerequisite.

## Local workflow

1. Run `Build-Test.py` with sudo in WSL. It builds an isolated image and restores the source, without restarting or changing the database.
2. Review build output and run `Activate-Test.py --check`.
3. During agreed maintenance with no online players, run `Activate-Test.py --activate --maintenance`. Previous image/source are retained for `--rollback --maintenance`. Rollback does not undo legitimate pet progress or purchases.
4. Close WoW and run `Install-Client.py --wow-closed`. The installer pins the existing TOC, backs up changes and adds StableBridge.lua. No MPQ change is required.
5. Publish launcher assets only after gameplay validation.

## In-game acceptance

- Roguetest: open a real stable master; verify Abomination name, level, current portrait and purchased slots. Store current, select its stored slot, retrieve, then relog and confirm pet/slots persist.
- Buy another slot: charge only the displayed native price, exactly once. Full stable and insufficient money must reject without pet loss.
- Swap two eligible pets and repeat with Demon and ordinary Beast; test Elemental/Dragonkin only where the existing family is already enabled. Verify names and skills survive.
- Non-Beast stable/portrait happiness stays hidden; Beast happiness remains available. No tooltip nil error.
- Close/reopen and switch to a Classic character: native controls must return. A late response must not reopen the bridge.
- Dead pet, out-of-range stable master, combat, mounted requests, invalid pet IDs and disabled family retrieval must reject. Secondary guardians never appear in the list.

Repository distribution contains only the new module header, minimal integration diff, addon and tests. Exported core files, live records and credentials are excluded.

The local build/activation commands above refer to the owner's pinned deployment package, not a fresh repository checkout. To integrate repository sources, add StableBridge.h alongside MoreMinions.cpp and apply stable-bridge.patch against the matching existing module; review any baseline difference instead of forcing the patch. The client installer targets the documented previous PTR addon revision. Test-Server.cpp exercises the real header with mocked APIs and empty include stubs for ScriptMgr.h, Chat.h, ChatCommand.h, WorldSession.h, WorldPacket.h, Opcodes.h and DBCStores.h; it is not a substitute for compiling against the core.
