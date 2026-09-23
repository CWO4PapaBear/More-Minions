# Captured minion name-save fix

Status: staged for compile check, not activated.

The PTR export shows character_pet.name is VARCHAR(21) and strict SQL mode is enabled. Borgoth the Bloodletter (16247) has a 23-character name. The capture path inherits that NPC name when there is no stock creature-family name. This exceeds the saved-pet column limit and explains a concrete save failure condition; the console export did not contain the underlying SQL error.

Before attaching/saving a newly captured custom minion, replace an overlong name with its reviewed family name (Abomination for family 203). If the family label is absent, empty or also overlong, use Companion. Count UTF-8 leading bytes to measure characters without truncating multibyte text. Short names, existing saved pets, stock Hunter capture and NPC templates are unchanged.

Build-Test.py builds against the reviewed active PTR source and restores it afterward. Stage-Server.py rejects source drift. Activate-Test.py provides image/source/port guards, zero-online-player maintenance checks, private startup validation and previous-image rollback. No SQL or client changes.

Acceptance: capture Borgoth with Dominate Undead, confirm name Abomination, recall/relog/stable and verify the approved skills remain. Capture a short-named eligible creature and confirm its name is retained. Existing pets must remain intact. Failure still preserves the original target.

This package is a PTR-specific staged overlay, not a portable full module release. Compile and in-game verification pending.
