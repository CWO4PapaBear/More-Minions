# Publishing the initial records

The local starter repository is separate from GitHub's initial README commit. Do not force-push it over that history.

Run this in Windows PowerShell from the local repository:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Publish.ps1
```

The script finds Git (including the installed Codex runtime copy), clones the existing GitHub repository into a sibling `More-Minions-publish` checkout, copies only tracked records, commits them on top of the existing history and pushes normally. It replaces the brief README as requested, preserves other existing files, and stops for unexpected local changes or authentication failures. Keep using that publishing checkout for future repository work.

Suggested GitHub About description:

> Planned WoW 3.3.5a companion module: early Beast training and Demon summoning, plus Dragonkin, Demon, Undead and Elemental pets. Interface records and server-development roadmap.

This initial publication is documentation, not a playable release. Do not attach client archives or publish an installable-module release yet.
