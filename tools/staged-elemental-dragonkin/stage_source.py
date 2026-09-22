"""Produce an isolated source candidate; never modify the supplied live file."""
import argparse
from pathlib import Path

BRIDGE = '''
Player* MoreMinionsScalingOwner(Unit* caster,unsigned spell){
 auto pet=caster?caster->ToPet():nullptr;
 if(!pet||!MoreMinions::Managed(pet)||!MoreMinions::ProfileReady(pet->GetEntry()))return nullptr;
 auto profile=MoreMinions::Profile(pet->GetEntry());
 if(!profile||(profile->type!=2&&profile->type!=4))return nullptr;
 auto owner=pet->GetOwner();auto group=MoreMinions::Origin(pet->GetUInt32Value(UNIT_CREATED_BY_SPELL));
 if(!owner||!group||!MoreMinions::Access(owner,*group))return nullptr;
 return MoreMinions::ProfileSkills(profile,pet->GetLevel()).count(spell)?owner:nullptr;
}
extern void AddMoreMinionsElementalDragonkinScripts();
'''

def patch(text):
    anchor='void Addmod_more_minionsScripts(){'
    tail='AddMoreMinionsDemonScripts();}'
    if 'MoreMinionsScalingOwner' in text or text.count(anchor)!=1 or text.count(tail)!=1:
        raise ValueError('Unreviewed or already patched module source')
    if 'std::set<unsigned> ProfileSkills(' not in text:
        raise ValueError('Approved Demon/Undead rank-selection prerequisite missing')
    return text.replace(anchor,BRIDGE+'\n'+anchor).replace(tail,'AddMoreMinionsDemonScripts();AddMoreMinionsElementalDragonkinScripts();}')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists() or args.output.resolve()==args.source.resolve():
        ap.error('A separate, new output file is required')
    result=patch(args.source.read_text());args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(result)
    print('Source candidate staged. No build or installation performed.')
