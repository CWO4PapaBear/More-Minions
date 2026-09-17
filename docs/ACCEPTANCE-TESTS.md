# Acceptance checklist

## Existing interface evidence

HeroFreePick 0.39.9 Lua 5.1 mock tests pass group cost/staging/refund/cancel, parent-only Shift previews, individual child icons/descriptions, Classic exclusion and mode/class restrictions. The catalog validator here checks five bundles, 26 children and Demon Mastery, not gameplay or visual rendering.

## Required server tests (not executed)

- Purchase permitted/denied by authoritative class, mode, level and budget. Retry/reconnect cannot double-charge or duplicate grants.
- Tame an allowlisted creature; reject wrong type, boss/protected/nonallowed entries, occupied/claimed targets and bad range/state.
- Interrupted tame grants no pet; successful tame creates exactly one owned pet and handles the original creature correctly.
- Existing active/stored pets are preserved; type switching and summoning do not duplicate or delete another pet.
- Pet death/revive, owner death, dismiss/recall, feeding if supported, action bar, AI and scaling behave correctly.
- Logout/login, server restart, map transfer and stable operations preserve ownership, skills and pet identity.
- Refund/reacquisition preserves agreed stored-pet policy and shared spell grants. Failure paths restore resources/state.
- Ordinary Demon Mastery summons and custom tamed Demons do not share incompatible ownership or pet records.
- Level-one Summon Imp works when authorized; later mastery members unlock at their own levels, with no extra FreePick cost.
- Hunter and non-Hunter Beast ownership both pass the complete lifecycle before adding other types.
- Each of the four new types passes the same lifecycle with at least one controlled creature entry.
- Classic without More Minions integration remains stock. Disabling optional features fails cleanly without corrupting saved pets.
- Client/server catalog mismatch is reported; no unsupported spell is offered as functional.

Record core commit, client patch hashes, configuration, test character/class/level, expected result, actual result and logs for every server test. Do not mark items passed from interface-only evidence.
