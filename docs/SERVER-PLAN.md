# Server development plan

## Target and boundaries

Target a pinned AzerothCore WoW 3.3.5a revision first. An optional module without core patches is the goal, not a verified capability. Audit native tame, summon, pet load/save, class checks and available script hooks on that exact revision before selecting the implementation path. Client spell records do not supply the original server logic.

Plan an independent server package (`mod-more-minions`), a versioned canonical catalog, and only the client spell/art support actually required. Add a separate HeroFreePick adapter for purchase/commit/notifications. Do not require its progression modules, Auto-Attack-Forever or Rune travel. Do not copy client archives wholesale or rely on their IDs being free.

The standalone access mechanism and price remain to be decided: config/trainer/quest or another authoritative route. FreePick AP/rarity accounting belongs to its integration. Both routes should call the same validated entitlement/grant service.

## Phases

1. **Baseline audit:** pin core/client revisions, inventory spell/creature IDs, identify available hooks and record whether any unavoidable core change is needed. Preserve a clean client and separate server database backup.
2. **One Beast lifecycle:** first prove a Hunter can acquire one allowed Beast, dismiss/recall, die/revive, log out/in and survive server restart. Then prove the same controlled lifecycle for a non-Hunter. Granting spell 1515 alone is not sufficient.
3. **Entitlements and transactions:** authoritative purchase validation, idempotent requests, persistence, source-aware shared spell grants, rollback/error reporting, safe access removal/reacquisition. No client-provided costs, class, ownership or targets may become authority.
4. **New types:** one allowlisted Dragonkin, Demon, Undead and Elemental, with explicit pet skills/scaling. Expand only after lifecycle tests pass. Ordinary Demon Mastery summons remain a distinct path and must coexist safely.
5. **FreePick integration:** commit approved purchases server-side, synchronize actual ownership back to the menu, grant level-eligible skills on login/level-up and preserve Classic behavior. Local preview selections are not entitlements.
6. **Standalone release:** configurable access, documented install/uninstall and migration, compatibility tests, asset review and a client/server version handshake if a patch is needed.

## Decisions to settle before gameplay implementation

- Supported core revision, hooks and whether stock pet persistence can represent every custom type.
- Creature allowlists; exclude protected NPCs/bosses and reject targets based on more than creature type.
- One active pet policy, switching types, stable/storage slots and interactions with existing Hunter/Warlock/Death Knight pets.
- Family/talents, scaling, diet/happiness, abilities, AI, action bar and player power/class requirements.
- Refund/removal behavior: preserve stored pet records by default rather than deleting them as an incidental UI action; confirm final policy.
- Spell ID allocation and client/server effects, interrupt/channel rules, targeting, pet creation and summon requirements.
- Standalone acquisition/price and which classes may use early Beast training and ordinary Demon summons.
- Asset license and project license before distributing implementation or artwork.

Do not deploy grant SQL or teach imported IDs before resolving collisions and native spell effects. Low imported IDs such as 884, 890 and 891 need the same scrutiny as high custom IDs. No compilation or server deployment is claimed by these records.
