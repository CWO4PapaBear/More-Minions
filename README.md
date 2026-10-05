# More Minions

Planned optional WoW 3.3.5a companion module: level-one Beast training and Demon summoning, plus Dragonkin, Demon, Undead and Elemental companions.

**Status: reference catalog plus PTR implementation overlays. This repository is not yet a self-contained installable pet module.** The September 23 changelog records successful PTR Undead/Demon stabling and store/retrieve/purchase testing. Some older foundation documents describe the September 17 state and must not be read as current implementation status.

## Area 52 integration in progress

`integrations/area52` contains the first porting step: a server-authoritative authorization adapter. It is opt-in through `MoreMinions.Area52.Enable = 1`, requires `CoA.Enable`, the `hero` class model, the `live` realm type, and a class-10 character. Authorization checks the learned parent spell on the server instead of the HeroFreePick addon's synthetic purchase IDs. Refund/removal revokes authorization immediately. The adapter does not grant spells, change costs or enable capture handlers by itself.

The six supported parent mappings cover Beast, Dragonkin, Demon, Undead, Elemental and Demon Mastery. PTR-only Beckon IDs and unknown bundles fail closed until their Area 52 equivalents are verified. Existing module checks still require learned control spells and valid pet ownership. `MoreMinions.RequireHeroAdapter` can remain enabled because this adapter supplies the authoritative callback.

Run `python integrations/area52/Test-Authorization.py` with a C++17 compiler for policy and adapter-contract tests. `Stage-Adapter.py --source /path/to/MoreMinions.cpp --output /new/stage` produces a separate candidate and refuses changed integration anchors. It never modifies the supplied PTR source. Copying these files alone is not a complete port: the existing module's core capture/save/load hooks, SQL, family definitions, spell shapes and Ascension client stable protocol require separate review and verification. The adapter is not activated on Area 52.

## What is recorded

- Five companion bundles, with 26 linked abilities, their current UI IDs, classes, costs, levels and icon references.
- Demon Mastery, including Summon Imp at level 1, recorded separately from the permanent Demon-taming bundle.
- Parent-only Shift expansion, skill previews, child badges, local planning/refunds and Classic exclusions already implemented in HeroFreePick.
- Wild Imp findings, unresolved server decisions and acceptance tests for the first working pet lifecycle.

## Start here

| Record | Purpose |
|---|---|
| [Current state](docs/CURRENT-STATE.md) | Implemented interface behavior versus unimplemented server behavior |
| [Ability catalog](docs/ABILITY-CATALOG.md) | Five bundles and Demon Mastery |
| [Machine-readable catalog](data/companion-catalog.json) | Snapshot of current FreePick definitions; reference IDs, not reserved server IDs |
| [Server plan](docs/SERVER-PLAN.md) | Standalone boundaries, phased development and open decisions |
| [Acceptance tests](docs/ACCEPTANCE-TESTS.md) | Required gameplay, persistence and integration checks |
| [Assets and evidence](docs/ASSETS-AND-EVIDENCE.md) | Provenance, artwork status and compatibility risks |

More Minions should work independently of HeroFreePick, Auto-Attack-Forever, Rune travel and the layout editor. HeroFreePick will be an optional integration client. Its AP/gem pricing does not automatically become a standalone purchase requirement. Classic HeroFreePick characters retain stock progression by default.

Run `python tools/validate_records.py` to check the catalog. This checks documentation consistency only, not gameplay. Selected server headers, integration diffs, addon sources and staged migration tools are now included; the complete PTR core and extracted client artwork are not distributed here.

Repository: https://github.com/CWO4PapaBear/More-Minions
Related interface project: https://github.com/CWO4PapaBear/HeroFreePick
