# Approved Demon and Undead family patch — 2026-09-22

Status: prepared for PTR build; not yet activated. The existing 701 live mappings are unchanged until deployment. This patch adds 190 approved mappings: 178 Demon and 12 Undead. Blocked rows are excluded.

- Felstalker (3102) stays in custom family 110, the Felhunter family (called Felhound in Ascension). It is not assigned to custom family 111, Felstalker. Its native family becomes 15 and its level remains 3–4.
- Vile Familiar (3101) becomes Demon, native Imp family 23/custom family 115, level 1–4. This affects every spawn using that template. Existing SmartAI, faction, loot and spawn positions are retained.
- Stock fallback profiles cover Imp, Fel Imp, Felhunter, Succubus, Voidwalker and Felguard. The separate Felstalker profile is available but receives no new mappings in this patch.
- Abyssals use the already-installed Infernal skill subset. Unsupported skills remain withheld.
- Pet skill selection and Lore use the highest eligible rank in each server spell chain. Stock unlock levels remain in effect: some low-level demons can melee before their first stock active skill unlocks.
- No additional Elemental/Dragonkin mappings are enabled by this patch. See [the second-pass reference review](ELEMENTAL-DRAGONKIN-SECOND-PASS.md).

No addon, MPQ or DBC update is required for this package. Creature-type changes can remain stale in an existing client cache; server Lore and capture checks are authoritative. World template changes also affect Classic world creatures, as explicitly requested; Classic capture spells are not changed.

## Deployment and rollback

`tools/staged-demon-undead-families` contains the reviewed plan and guarded scripts for this owner's existing classless-test PTR layout. These are not a general installer for arbitrary servers. They expect the existing More Minions module, imported definitions and prior neutral-capture patch.

Build validates database baselines, saves before/after source, compiles a separate image and restores source. It does not restart the server or write database rows. Activation is a separate maintenance step with zero online characters, image/source/port guards, transactional mapping/template changes, private startup validation and restoration of public ports. Rollback restores the previous image, source and exactly the affected database records. Unrelated database drift stops the operation for review.

Validation completed locally: Python syntax, baseline preflight fixtures for before/after states and rejection of a changed mapping; all 190 mappings resolve to staged profiles. Actual C++ compilation, live SQL and in-game behavior remain pending the PTR build and activation.

## PTR test notes (publish after activation)

- Capture neutral attackable and hostile eligible Demons/Undead; friendly/protected targets must remain blocked.
- Check Felstalker and Vile Familiar with Demon Lore, then capture at an eligible character level.
- Check family skills, rank upgrades, autocast, relogging and Hunter-style stable storage.
- Confirm one primary companion and the existing independent Demon Mastery companion still work together.
- Test existing mapped pets for regressions, especially spell-bar ranks after leveling.

## Activation collation fix

The first PTR activation encountered MySQL error 1267 while comparing text with different implicit collations. Transaction rollback and startup of the previous image completed. Guard comparisons now cast both operands to binary for exact equality, including the rollback review note. Database/schema collations and the approved mapping plan remain unchanged. The SQL-only tool revision requires no C++ rebuild; deployment still awaits a successful activation retry. Generated forward/rollback guards and the local deployment-tool hash were checked; live SQL retry remains pending.
