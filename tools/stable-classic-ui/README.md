# Restore the classic stable interface

The owner confirmed the server-backed Store, Retrieve and Purchase transactions work on PTR. The first bridge UI used a replacement panel to bypass missing native client stable records; its layout and changing active/stored icons were rejected.

This client-only follow-up retains the verified `.mmstable` transport and populates the original current-pet box, four stable slots, Purchase button, cost display, labels, model and frame art. It creates no visible replacement panel, buttons or labels and does not reposition the native controls.

- Select a pet to view it. Drag between the current box and a purchased stable slot to store, retrieve or swap. Alternatively select the occupied box, then click the empty destination box.
- The server chooses the first free stable slot for storage, as its existing native handler does. Rearranging stored pets between two storage slots is not implemented.
- The same creature-type icon is used for a pet in both current and stored boxes. The previous live-head portrait could not remain available after the live unit disappeared. The large model still displays the selected creature.
- Happiness remains limited to the current Beast; Undead, Demon, Elemental and Dragonkin do not show it.
- Characters outside the imported capture system keep the original click and drag handlers. Global stable APIs remain unchanged.

Local Lua 5.1 tests passed for native-control reuse, unchanged layout, click and drag commands, repeated-request suppression, purchasing, stored model selection, icon consistency, Beast-only happiness, stale replies, timeout and native fallback. Isolated installer, idempotency and drift refusal passed. Actual in-game drag/event behavior and final appearance require owner testing.

Close WoW and run the pinned Install-Client.py with `--wow-closed`. Only MoreMinionsDemon/StableBridge.lua changes. No server rebuild/restart, SQL or MPQ change. The existing activated server bridge is required. Launcher publication remains pending.
