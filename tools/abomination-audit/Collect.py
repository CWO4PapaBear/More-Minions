"""Read-only Abomination NPC spell/AI export; no restart or database writes."""
import argparse,csv,hashlib,io,json,re,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--output',required=True,type=Path)
 p.add_argument('--server-root',type=Path,default=Path('/home/dml/games/wow-server-classless-test'))
 a=p.parse_args()
 if a.output.exists():p.error('Use a new output directory')
 a.output.mkdir(parents=True)
 manifest={'status':'read-only export','files':{},'missing':[]}
 def save(name,data):
  f=a.output/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
  manifest['files'][name]=hashlib.sha256(data).hexdigest()
 def query(name,sql):
  result=subprocess.run(['docker','exec','-i','classless-test-database','sh','-c','MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot --batch acore_world'],input=sql.encode(),capture_output=True,timeout=180)
  if result.returncode:
   manifest['missing'].append(name+': '+result.stderr.decode(errors='replace')[-500:]);return []
  save(name,result.stdout)
  return list(csv.DictReader(io.StringIO(result.stdout.decode()),delimiter='\t'))
 ids=json.loads((Path(__file__).parent/'entries.json').read_text())
 templates=query('templates.tsv','SELECT * FROM creature_template WHERE entry IN ('+','.join(map(str,ids))+") OR name LIKE '%Abomination%';")
 if not templates:raise RuntimeError('No template data; see database access/error')
 ids=sorted({int(r['entry']) for r in templates})
 # Difficulty variants can have different spells or compiled scripts.
 extra={int(r.get(k,'0')) for r in templates for k in ('difficulty_entry_1','difficulty_entry_2','difficulty_entry_3')}-{0}-set(ids)
 if extra:
  templates+=query('difficulty-templates.tsv','SELECT * FROM creature_template WHERE entry IN ('+','.join(map(str,sorted(extra)))+');')
  ids=sorted(set(ids)|extra)
 selected=','.join(map(str,ids))
 spawns=query('spawns.tsv','SELECT * FROM creature WHERE id IN ('+selected+');')
 guids=','.join(str(int(r['guid'])) for r in spawns) or '0'
 query('smart-scripts.tsv','SELECT * FROM smart_scripts WHERE (source_type=0 AND (entryorguid IN ('+selected+') OR entryorguid IN (SELECT -guid FROM creature WHERE id IN ('+selected+')))) OR source_type=9;')
 # All timed action lists are retained so nested/random list calls are not missed.
 query('template-addons.tsv','SELECT * FROM creature_template_addon WHERE entry IN ('+selected+');')
 query('spawn-addons.tsv','SELECT * FROM creature_addon WHERE guid IN ('+guids+');')
 tables={next(iter(r.values())) for r in query('tables.tsv','SHOW TABLES;')}
 for table in ('creature_template_spell','creature_equip_template'):
  if table in tables:
   cols=query(table+'-schema.tsv','SHOW COLUMNS FROM '+table+';')
   key=next((r['Field'] for r in cols if r['Field'].lower() in ('creatureid','entry','creature_id')),None)
   if key:query(table+'.tsv','SELECT * FROM '+table+' WHERE `'+key+'` IN ('+selected+');')
 query('spell-overrides.tsv','SELECT * FROM spell_dbc;')
 query('spell-bindings.tsv','SELECT * FROM spell_script_names;')
 names={r.get('ScriptName','') for r in templates}-{''}
 matched=[]
 for base in (a.server_root/'src/server/scripts',a.server_root/'modules'):
  for f in base.rglob('*.cpp'):
   text=f.read_text(errors='replace')
   if any('"'+name+'"' in text or re.search(r'\b'+re.escape(name)+r'\b',text) for name in names):
    rel=f.relative_to(a.server_root).as_posix();save(rel,f.read_bytes());matched.append(rel)
 manifest['scriptNames']=sorted(names);manifest['matchedSourceFiles']=matched
 for name in ('Spell','SpellDuration','CreatureSpellData'):
  r=subprocess.run(['docker','exec','classless-test-worldserver','cat','/azerothcore/env/dist/data/dbc/'+name+'.dbc'],capture_output=True,timeout=180)
  if r.returncode:manifest['missing'].append(name+'.dbc: '+r.stderr.decode(errors='replace')[-300:])
  else:save(name+'.dbc',r.stdout)
 r=subprocess.run(['docker','inspect','--format','{{.Image}}','classless-test-worldserver'],capture_output=True,text=True,check=True)
 manifest['image']=r.stdout.strip();manifest['entries']=ids
 (a.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('ABOMINATION NPC AUDIT EXPORT COMPLETE:',a.output)
 if manifest['missing']:print('Review missing reads in manifest.json.')
 print('No restart, database writes, spell grants or client changes.')

if __name__=='__main__':main()
