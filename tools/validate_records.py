from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'data/companion-catalog.json').read_text())
assert len(c['bundles'])==5
assert {b['name'] for b in c['bundles']}=={'Tame Beast','Tame Dragonkin','Enslave Demon','Dominate Undead','Tether Elemental'}
assert sum(len(b['members']) for b in c['bundles'])==26
ids=set()
for b in c['bundles']:
 assert b['ae']==4 and b['rarityCost']==2 and b['quality']=='Epic' and b['level']==1
 for child in b['members']:
  assert child['requiredBundle']==b['id'] and child['ae']==0 and child['level']==1
  assert child['id'] not in ids;ids.add(child['id'])
m=c['demonMastery'];assert m['ae']==2 and m['rarityCost']==2 and m['level']==1
assert len(m['members'])==5
imp=next(x for x in m['members'] if 688 in x['spellIds']);assert imp['level']==1
assert all(x['requiredMastery']==m['id'] and x['ae']==0 for x in m['members'])
assert c['wildImps']['status'].startswith('Research only')
for p in root.rglob('*'):
 if '.git' in p.parts:continue
 assert p.suffix.lower() not in ('.mpq','.dbc','.blp','.exe'),p
print('PASS: five bundles, 26 child abilities, independent Demon Mastery, level/cost rules and no extracted binary assets.')
