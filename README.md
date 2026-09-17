# More Minions

Planned optional WoW 3.3.5a companion module: level-one Beast training and Demon summoning, plus Dragonkin, Demon, Undead and Elemental companions.

**Status: design and interface records. Server implementation has not started. This repository is not an installable pet module.** The existing work is in the HeroFreePick planning interface; selecting a package there does not teach server spells, tame a creature or create a persistent pet.

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

Run `python tools/validate_records.py` to check the catalog. This checks documentation consistency only, not gameplay. No server source, SQL migration, executable, client patch or extracted artwork is shipped yet.

Repository: https://github.com/CWO4PapaBear/More-Minions
Related interface project: https://github.com/CWO4PapaBear/HeroFreePick
