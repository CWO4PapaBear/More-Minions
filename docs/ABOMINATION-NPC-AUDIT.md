# Abomination NPC ability audit

Status: read-only collector prepared; live export pending.

The audit selects 125 reference entries plus templates named Abomination and their difficulty variants. It gathers template spell slots, separate spell tables when present, spawn-specific and template SmartAI, all timed action lists for dependency tracing, addon auras, spell overrides, spell script bindings and matching compiled creature scripts. Spell and CreatureSpellData DBCs are captured for decoding. The export is local review material and must not be committed.

NPC ability evidence will be kept separate from imported Ascension pet abilities. Scripted boss mechanics are not automatically suitable for player pets. Nested compiled spell handlers may require a follow-up source read once IDs are resolved. No database or client modifications are performed.

The collector explicitly requests utf8mb4 from MySQL. Unexpected invalid UTF-8 is recorded in encodingWarnings and escaped during parsing; the original exported bytes remain unchanged. This was checked against the actual SmartAI export that caused the decoding failure. Reruns use a fresh output folder to preserve partial exports.
