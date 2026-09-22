"""Guarded world-only changes for the approved mapping set."""
import csv,io,json,subprocess,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent
NOTE='Approved demon-undead families 20260922'

def query(sql):
 p=subprocess.run(['docker','exec','-i','classless-test-database','sh','-c','MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot --batch acore_world'],input=sql,text=True,capture_output=True,timeout=120)
 if p.returncode:raise RuntimeError('World SQL failed: '+p.stderr[-1500:])
 return list(csv.DictReader(io.StringIO(p.stdout),delimiter='\t'))

def value(v):
 return "CONVERT(0x"+str(v).encode().hex()+" USING utf8mb4)" if str(v) else "''"

def plan():return json.loads((HERE/'approved-plan.json').read_text())
def equal(column,v):return 'CAST('+column+' AS BINARY)=CAST('+value(v)+' AS BINARY)'

def condition(row):return ' AND '.join(equal('`'+k+'`',v) for k,v in row.items())
def ids(p):return ','.join(str(r['entry']) for r in p['mappings'])
def engines():
 rows=query("SELECT TABLE_NAME,ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='acore_world' AND TABLE_NAME IN ('creature_template','more_minions_creature_family');")
 if len(rows)!=2 or any(r['ENGINE']!='InnoDB' for r in rows):raise RuntimeError('Transactional world tables required')

def check(mode='before'):
 p=plan();engines();rows=query('SELECT * FROM more_minions_creature_family WHERE creature_entry IN ('+ids(p)+');')
 if mode=='before' and rows:raise RuntimeError('A proposed mapping already exists; reconcile before activation')
 if mode=='after':
  expected={(str(r['entry']),str(r['family'])) for r in p['mappings']}
  if {(r['creature_entry'],r['family_id']) for r in rows}!=expected or any(r['enabled']!='1' or r['review_note']!=NOTE for r in rows):raise RuntimeError('Installed mappings differ')
 templates={r['entry']:r for r in query('SELECT * FROM creature_template WHERE entry IN ('+ids(p)+');')}
 updates={str(r['entry']):r for r in p['templateUpdates']}
 for original in p['expectedTemplates']:
  expected=dict(original)
  if mode=='after':expected.update({k:str(v) for k,v in updates.get(original['entry'],{}).items()})
  if any(templates.get(original['entry'],{}).get(k)!=v for k,v in expected.items()):raise RuntimeError('Creature template changed: '+original['entry'])

def change(rollback=False):
 p=plan();engines()
 if rollback:
  rows=query('SELECT creature_entry FROM more_minions_creature_family WHERE creature_entry IN ('+ids(p)+');')
  if not rows:
   check('before');return
  check('after')
 else:check('before')
 proc='mm_family_'+uuid.uuid4().hex
 body=['DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;','START TRANSACTION;']
 templates={r['entry']:r for r in p['expectedTemplates']};updates={str(r['entry']):r for r in p['templateUpdates']}
 for original in p['expectedTemplates']:
  expected=dict(original)
  if rollback:expected.update(updates.get(original['entry'],{}))
  body.append("IF (SELECT COUNT(*) FROM creature_template WHERE "+condition(expected)+") <> 1 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Template changed during activation'; END IF;")
 for r in p['mappings']:
  where='creature_entry='+str(r['entry'])
  if rollback:
   where+=' AND family_id='+str(r['family'])+' AND enabled=1 AND '+equal('review_note',NOTE)
   body.append("IF (SELECT COUNT(*) FROM more_minions_creature_family WHERE "+where+") <> 1 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Mapping changed during rollback'; END IF;")
   body.append('DELETE FROM more_minions_creature_family WHERE '+where+';')
  else:
   body.append("IF (SELECT COUNT(*) FROM more_minions_creature_family WHERE "+where+") <> 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Mapping collision'; END IF;")
   body.append('INSERT INTO more_minions_creature_family (creature_entry,family_id,enabled,review_note) VALUES ('+str(r['entry'])+','+str(r['family'])+',1,'+value(NOTE)+');')
 for update in p['templateUpdates']:
  target={k:templates[str(update['entry'])][k] if rollback else v for k,v in update.items() if k!='entry'}
  body.append('UPDATE creature_template SET '+','.join('`'+k+'`='+value(v) for k,v in target.items())+' WHERE entry='+str(update['entry'])+';')
 body.append('COMMIT;')
 statement='DELIMITER $$\nCREATE PROCEDURE '+proc+'() BEGIN\n'+'\n'.join(body)+'\nEND$$\nDELIMITER ;\nCALL '+proc+'();\n'
 try:query(statement)
 finally:query('DROP PROCEDURE IF EXISTS '+proc+';')
 check('before' if rollback else 'after')
