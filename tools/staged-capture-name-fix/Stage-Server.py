FILES={'modules/mod-more-minions/src/MoreMinions.cpp': [(' p->SetMinion(pet,true);pet->SetReactState(REACT_DEFENSIVE);pet->SetFullHealth();', ' // character_pet.name is VARCHAR(21). Preserve short localized names; use\n // the reviewed family name for longer NPC names instead of failing the save.\n auto nameLength=[](std::string const& name){return std::count_if(name.begin(),name.end(),[](unsigned char ch){return (ch&0xC0)!=0x80;});};\n if(nameLength(pet->GetName())>21){\n  auto profile=Profile(pet->GetEntry());\n  std::string safeName=profile?profile->name:"Companion";\n  if(safeName.empty()||nameLength(safeName)>21)safeName="Companion";\n  pet->SetName(safeName);\n }\n p->SetMinion(pet,true);pet->SetReactState(REACT_DEFENSIVE);pet->SetFullHealth();')]}
BASELINE_SHA256='745241d379f8b2ae9e06b521b86b91fc57b15e4180e32d99f927ccff91d13a77'

import hashlib
def patch(source,changes):
 if hashlib.sha256(source.encode()).hexdigest()!=BASELINE_SHA256:raise ValueError('Current MoreMinions source differs from reviewed active Abomination build')
 for before,after in changes:
  if source.count(before)!=1:raise ValueError('Capture save anchor changed')
  source=source.replace(before,after)
 return source
