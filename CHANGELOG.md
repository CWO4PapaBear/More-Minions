## Staged server-backed stable controls

Build follow-up: qualify the command table and console flag with `Acore::ChatCommands`. The first full PTR compile caught the missing namespace; source restoration succeeded and no activation occurred. Contract tests now use the same namespace instead of global stand-ins. Local recheck passed; full rebuild pending.

Add a More Minions stable bridge for imported primary pets whose native client stable list is empty. Store, retrieve/swap and buy actions use the existing server handlers, with access, proximity and pet ownership checks. Demon, Undead, Elemental and Dragonkin share the interface without enabling withheld families or stabling secondary guardians. Non-Beast happiness is hidden; current pet portraits use the live unit.

Lua 5.1 lifecycle/action tests, mocked C++ command-contract tests and isolated installer checks passed. Full PTR build, activation, gameplay validation and launcher publication remain pending. See [stable bridge](tools/stable-bridge/README.md).

## Staged Beast-only happiness UI

Hide happiness/diet controls for non-Beast companions. Stable current-pet fallback uses the live portrait rather than a whistle. Display tests passed and local installation completed. The server-backed stable candidate above addresses the remaining transaction problem; launcher publication remains pending.

## Stable live-primary display follow-up

Live diagnostics showed the client exposes no slot-0 record for the Abomination. Use the permanent primary pet unit for stable display and scoped icon/family fallback; leave native slot data and server transactions unchanged. Reference UI tests pass; in-game transactions and launcher publication pending.

## Staged stable UI compatibility

Add a narrowly scoped client adapter for server-listed primary companions with imported capture abilities. Covers Demon, Undead, Elemental and Dragonkin stable display and purchase controls. Lua 5.1 reference-UI and installer tests passed; live store/retrieve and launcher publication pending. See tools/stable-client-compatibility.

# Changelog

## Unreleased — repository foundation

- Document the existing FreePick companion interface work and explicit server gaps.
- Record five companion bundles / 26 members and separate five-member Demon Mastery.
- Establish standalone boundaries, phased server plan and acceptance checklist.
- Preserve Wild Imp research as an open separate feature rather than an invented bundle.
- Add catalog consistency checks and a publishing helper that preserves remote history.
