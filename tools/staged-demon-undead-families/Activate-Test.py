"""Activate the reviewed Demon/Undead family image. Guarded world mapping and Valley template changes; no client installation."""
from pathlib import Path
import argparse,copy,hashlib,json,os,shutil,subprocess,time
import Database
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/dml/games/wow-server-classless-test');WORLD='classless-test-worldserver';DB='classless-test-database'
REL='modules/mod-hero-starting-path/src/StartingPath.cpp'
def run(args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=180)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p.stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):p.write_text(json.dumps(data,indent=2));os.chmod(p,0o600)
def inspect():return json.loads(run(['docker','inspect',WORLD]))[0]
def sql(query):return run(['docker','exec',DB,'sh','-c','MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot --batch --skip-column-names acore_characters -e "$1"','demon-undead-families-read',query])
def compose(config):run(['docker','compose','-p','classless-test','-f',str(config),'up','-d','--no-deps','--no-build','--force-recreate','ac-worldserver'])
def ready(image,path):
 for i in range(180):
  w=inspect();logs=run(['docker','logs',WORLD]);path.write_text(logs)
  if not w['State']['Running'] or w['Image']!=image:raise RuntimeError('Unexpected world state; see startup log')
  if any(('validation failed' in line.lower() or 'baseline mismatch' in line.lower() or 'must rollback' in line.lower()) and any(tag in line for tag in ('HERO_','MORE_MINIONS')) for line in logs.splitlines()):raise RuntimeError('Module validation failed; see startup log')
  if all(marker in logs for marker in ('HERO_STARTING_PATH ready v6.7;', 'HERO_DK_SCALING v1 ready;', 'MORE_MINIONS v0.2 staged handlers ready; shared Hunter stable', 'MORE_MINIONS independent Demon Mastery ready (native stable slot preserved)', 'HERO_PROJECTILES v0.4 loaded;')):
   test=subprocess.run(['docker','exec',WORLD,'bash','-c','exec 3<>/dev/tcp/127.0.0.1/8085'],capture_output=True)
   if test.returncode==0:return
  if i%6==0:print('Waiting for world startup...',flush=True)
  time.sleep(5)
 raise RuntimeError('World startup timeout; see '+str(path))
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--check',action='store_true');g.add_argument('--activate',action='store_true');g.add_argument('--rollback',action='store_true');p.add_argument('--maintenance',action='store_true');a=p.parse_args()
 if os.name!='posix' or os.geteuid()!=0:p.error('Run with sudo python3 in WSL.')
 if not a.check and not a.maintenance:p.error('Arrange downtime and supply --maintenance.')
 import fcntl
 lock=(ROOT/'.hero-upcoming-build.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 s=json.loads((HERE/'build-state.json').read_text());assert sha(HERE/'approved-plan.json')==s['planSHA256'] and sha(HERE/'Database.py')==s['databaseToolSHA256'],'Database plan changed since build';work=Path(s['work']);assert work.resolve().is_relative_to(ROOT/'backups')
 w=inspect();assert w['Config']['Labels'].get('com.docker.compose.project')=='classless-test'
 assert not s['sourceRestorationErrors'] and s['status']=='compiled-not-activated'
 expected={'modules/mod-more-minions/src/MoreMinions.cpp','modules/mod-more-minions/src/FamilyProfiles.h'}
 assert set(s['files'])==expected,'Unexpected source scope'
 for rel,h in s['files'].items():
  assert sha(work/'before'/rel)==h['before'] and sha(work/'after'/rel)==h['after'],'Build backup differs: '+rel
 def copy_source(version):
  for rel in s['files']:shutil.copy2(work/version/rel,ROOT/rel)
 def rollback():
  assert inspect()['Image'] in (s['previousImage'],s['builtImage'])
  for rel,h in s['files'].items():assert sha(ROOT/rel) in (h['before'],h['after'])
  run(['docker','stop',WORLD]);Database.change(rollback=True);copy_source('before');compose(work/'demon-undead-families-rollback.json')
  ready(s['previousImage'],HERE/'rollback.log');assert inspect()['HostConfig']['PortBindings']==s['ports']
  save(HERE/'activation.json',{'phase':'rolled-back','image':s['previousImage']});print('ROLLBACK COMPLETE. Previous image/source and affected world rows restored.')
 if a.rollback:
  assert sql('SELECT COUNT(*) FROM characters WHERE online=1;')=='0','Players online; arrange maintenance first'
  rollback();return
 if w['Image']==s['builtImage']:
  assert w['HostConfig']['PortBindings']==s['ports'],'Installed image has unexpected ports; stop for review'
  for rel,h in s['files'].items():assert sha(ROOT/rel)==h['after'],'Installed image source differs: '+rel
  assert w['Config']['Labels']['com.docker.compose.project.config_files']==str(work/'demon-undead-families-active.json'),'Installed image uses an unexpected compose configuration'
  Database.check('after');ready(s['builtImage'],HERE/'already-active-check.log')
  print('ALREADY ACTIVE: Demon/Undead family image, source, ports and readiness verified. No restart or changes performed.')
  return
 assert w['Image']==s['previousImage'],'Live image changed since build; neither previous nor Demon/Undead family image is running. Stop for review.'
 assert w['HostConfig']['PortBindings']==s['ports'],'Live ports changed since build'
 for rel,h in s['files'].items():assert sha(ROOT/rel)==h['before'],'Live source changed since build: '+rel
 assert run(['docker','image','inspect','--format','{{.Id}}',s['tag']])==s['builtImage']
 assert w['Config']['Labels']['com.docker.compose.project.config_files']==s['activeConfig'],'Live compose changed'
 config=json.loads(run(['docker','compose','-p','classless-test','-f',s['activeConfig'],'config','--format','json']))
 old=copy.deepcopy(config);old['services']['ac-worldserver'].pop('build',None);old['services']['ac-worldserver']['image']=s['previousImage']
 new=copy.deepcopy(old);new['services']['ac-worldserver']['image']=s['builtImage']
 private=copy.deepcopy(new);private['services']['ac-worldserver']['ports']=[]
 for name,data in [('rollback',old),('active',new),('private',private)]:
  path=work/('demon-undead-families-'+name+'.json');save(path,data);run(['docker','compose','-p','classless-test','-f',str(path),'config','--quiet'])
 Database.check('before')
 if a.check:print('ACTIVATION CHECK PASSED. Image/source/ports verified. Server unchanged.');return
 assert sql('SELECT COUNT(*) FROM characters WHERE online=1;')=='0','Players online; log them out before activation'
 try:
  run(['docker','stop',WORLD]);Database.change();copy_source('after')
  save(HERE/'activation.json',{'phase':'private-validation','image':s['builtImage']})
  compose(work/'demon-undead-families-private.json');ready(s['builtImage'],HERE/'private-startup.log')
  assert not inspect()['HostConfig']['PortBindings'],'Private startup unexpectedly published ports'
  compose(work/'demon-undead-families-active.json');ready(s['builtImage'],HERE/'startup.log')
  assert inspect()['HostConfig']['PortBindings']==s['ports'],'Published ports differ'
 except BaseException:
  rollback();raise
 save(HERE/'activation.json',{'phase':'active','image':s['builtImage'],'previousImage':s['previousImage'],'work':str(work)})
 print('ACTIVATION COMPLETE: 190 approved Demon/Undead mappings and Valley creature changes installed. No DBC, MPQ or addon files changed. Previous image retained.')
if __name__=='__main__':main()
