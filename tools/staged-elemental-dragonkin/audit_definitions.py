"""Audit first-wave source definitions and dependencies; never install files."""
import argparse, csv, hashlib, json, struct
from pathlib import Path
HERE=Path(__file__).resolve().parent

def dbc(path):
    b=path.read_bytes();magic,n,f,size,strings=struct.unpack_from('<4s4I',b)
    if magic!=b'WDBC' or size!=f*4 or len(b)!=20+n*size+strings:
        raise ValueError('Malformed DBC: '+str(path))
    return {r[0]:r for r in struct.iter_unpack('<'+str(f)+'I',b[20:20+n*size])}

def audit(plan,records,baseline):
    records={r['id']:r for r in records}
    live=dbc(baseline/'Spell.dbc')
    sql={int(r['ID']) for r in csv.DictReader((baseline/'spell_dbc_ids.tsv').open(),delimiter='\t')}
    tables={'SpellDuration':(40,), 'SpellRange':(46,), 'SpellRadius':(92,93,94),
            'SpellCastTimes':(28,), 'SpellIcon':(133,134), 'SpellVisual':(131,132)}
    available={t:dbc(baseline/(t+'.dbc')) for t in tables}
    result=[]
    for rule in plan['spells']:
        r=records[rule['id']];v=r['rawUInt32Fields']
        digest=hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()
        if digest!=rule['sourceDefinitionSHA256'] or v[71:74]!=[2,0,0] or r['dependencies']:
            raise ValueError('Source definition changed or unsupported: '+str(rule['id']))
        refs={t:sorted({v[i] for i in fields}-{0}) for t,fields in tables.items()}
        result.append({'id':rule['id'],'name':rule['name'],
            'existingDBC':rule['id'] in live,'existingSQL':rule['id'] in sql,
            'required':refs,'missing':{t:[i for i in ids if i not in available[t]] for t,ids in refs.items()}})
    return {'status':'audit only; auxiliary ID presence does not establish matching contents',
            'baselineSpellSHA256':hashlib.sha256((baseline/'Spell.dbc').read_bytes()).hexdigest(),
            'spells':result,'remaining':['auxiliary row comparison and assets','fresh binding/proc/bonus collision export',
            'client tooltip formula rendering','creature mappings','C++ build','combat and stable tests']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--records',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('Use a new output file')
    report=audit(json.loads((HERE/'plan.json').read_text()),json.loads(a.records.read_text())['records'],a.baseline)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print('First-wave definition audit complete. No server or client changes.')
