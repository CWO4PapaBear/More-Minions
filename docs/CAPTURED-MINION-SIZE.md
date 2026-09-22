# Captured minion size correction

Status: staged; not built or activated.

Captured custom minions occupy the Hunter pet slot. The core consequently applies CreatureFamily level-dependent size scaling, which can shrink low-level captured demons. The patch routes pets tagged with a More Minions capture origin through the normal database creature-size calculation instead. Stock Hunter pets and summoned Warlock pets retain their existing sizing. This is normal database sizing, not preservation of temporary size auras on a wild target.

The core sizing function is used during pet initialization and later size recalculation, so the correction is intended to survive relogging, stable retrieval and leveling. Existing captured pets should not need to be retamed. Verify Vile Familiar and Felstalker after recall, relog and stable retrieval; also verify a stock Hunter beast is unchanged.

Python syntax and guarded source replacement tests passed against the exported core, including rejection of repeat application. C++ compilation and in-game behavior remain unverified. Build and activation scripts are scoped to the existing PTR layout. No SQL, DBC, addon or client update is required.
