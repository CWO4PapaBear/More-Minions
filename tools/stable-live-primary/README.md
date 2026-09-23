# Live primary pet stable display follow-up

The live diagnostic confirmed HasPetUI returns 1/nil, Dominate Undead is known, the stable is open, and every GetStablePetInfo entry is empty. The first compatibility attempt required a slot-0 record, so its override never activated.

This revision uses the live permanent primary pet GUID (F140) plus an imported capture ability to enable stable display. Scoped icon/family fallbacks populate the native active pet panel; it does not invent stable slot records or replace global pet APIs. Server handlers still decide whether any pet can actually be stored or retrieved. Secondary guardian GUIDs (F130), and ordinary clients without capture spells, do not receive this override.

Reference-UI tests now reproduce empty slot-0 data, validate active pet display and purchase controls for all four capture groups, and verify guardian exclusion and unchanged native slot data. This does not prove live stable transactions work. Close WoW, install with Install-Client.py --wow-closed, then test purchase, store, retrieve and relog. If any operation fails, run /mmstable while the window is open and /reload to save updated diagnostics. No server restart or MPQ changes. Launcher publication pending successful in-game verification.
